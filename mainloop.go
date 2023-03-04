package main

import (
	"encoding/json"
	"fmt"
	"github.com/trojsten/ksp-proboj/libproboj"
)

// Tick executes one game tick
func (w *World) Tick() {
	for i, player := range w.Players {
		if player.Alive == false {
			continue
		}
		w.Runner.ToPlayer(player.Name, fmt.Sprintf("TICK %d", w.TickNumber), w.DataForPlayer(player))
		resp, data := w.Runner.ReadPlayer(player.Name)
		if resp != libproboj.Ok {
			w.Runner.Log(fmt.Sprintf("bad response while reading player %s: %d", player.Name, resp))
			continue
		}
		w.Runner.Log(data)
		err := w.ParseResponse(data, &w.Players[i])
		if err != nil {
			w.Runner.Log(fmt.Sprintf("error while parsing response from %s: %s", player.Name, err.Error()))
			continue
		}
	}

	// Bullet time!
	var bullets []Bullet
	for i := range w.Bullets {
		bullet := &w.Bullets[i]
		var success, bulletMovement = bullet.Tick(w)
		if success {
			bullets = append(bullets, *bullet)
			w.BulletMovements = append(w.BulletMovements, bulletMovement)
		}
	}
	w.Bullets = bullets

	// Update players
	for i := range w.Players {
		w.Players[i].Tick()
	}

	for i, playerMovement := range w.PlayerMovements {
		for _, entityMovement := range w.EntityMovement {
			if intersect(playerMovement.OldPosition, playerMovement.Player.Position, playerMovement.Player.Tank.Radius(),
				entityMovement.OldPosition, entityMovement.Entity.Position, entityMovement.Entity.Radius) {
				w.Runner.Log(fmt.Sprintf("Player (id: %d) and Entity (%f %f) intersects\n", playerMovement.Player.Id, entityMovement.Entity.X, entityMovement.Entity.Y))
				playerMovement.Player.Health -= PlayerEntityCollisionHealth
			}
		}
		for _, bulletMovement := range w.BulletMovements {
			if bulletMovement.Bullet.ShooterId != i && intersect(playerMovement.OldPosition, playerMovement.Player.Position, playerMovement.Player.Tank.Radius(),
				bulletMovement.OldPosition, bulletMovement.Bullet.Position, bulletMovement.Bullet.Radius) {
				w.Runner.Log(fmt.Sprintf("Player (id: %d) and Bullet (%f %f) intersects\n", playerMovement.Player.Id, bulletMovement.Bullet.X, bulletMovement.Bullet.Y))
				w.Players[bulletMovement.Bullet.ShooterId].Exp += int(bulletMovement.Bullet.Damage * PlayerHitExpCoefficient)
				bulletMovement.Bullet.TTL -= BulletCollisionTTL
				playerMovement.Player.Health -= bulletMovement.Bullet.Damage
			}
		}
		for j, playerMovement2 := range w.PlayerMovements {
			if i != j && intersect(playerMovement.OldPosition, playerMovement.Player.Position, playerMovement.Player.Tank.Radius(),
				playerMovement2.OldPosition, playerMovement2.Player.Position, playerMovement2.Player.Tank.Radius()) {
				w.Runner.Log(fmt.Sprintf("Player (id: %d) and Player (id: %d) intersects\n", playerMovement.Player.Id, playerMovement2.Player.Id))
				playerMovement.Player.Health -= PlayerPlayerCollisionHealth
			}
		}
	}

	for _, bulletMovement := range w.BulletMovements {
		for _, entityMovement := range w.EntityMovement {
			if intersect(bulletMovement.OldPosition, bulletMovement.Bullet.Position, bulletMovement.Bullet.Radius,
				entityMovement.OldPosition, entityMovement.Entity.Position, entityMovement.Entity.Radius) {
				w.Runner.Log(fmt.Sprintf("Bullet (%f %f) and Entity (%f %f) intersects\n", bulletMovement.Bullet.X, bulletMovement.Bullet.Y, entityMovement.Entity.X, entityMovement.Entity.Y))
				w.Players[bulletMovement.Bullet.ShooterId].Exp += int(bulletMovement.Bullet.Damage * EntityHitExpCoefficient)
				bulletMovement.Bullet.TTL -= BulletCollisionTTL
				entityMovement.Entity.Radius -= bulletMovement.Bullet.Damage * BulletEntityCollisionRadiusCoefficient
			}
		}
	}

	w.PlayerMovements = nil
	w.BulletMovements = nil
	w.EntityMovement = nil

	data, err := json.Marshal(w)
	if err != nil {
		w.Runner.Log(fmt.Sprintf("could not marshal data for observer: %s", err.Error()))
	}
	w.Runner.ToObserver(string(data))
}
