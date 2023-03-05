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
	bullets := []Bullet{}
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
		playerSegment := Segment{playerMovement.OldPosition, playerMovement.Player.Position}

		for j, entity := range w.Entities {
			entitySegment := Segment{entity.Position, entity.Position}
			if Collides(playerSegment, playerMovement.Player.Tank.Radius(), entitySegment, entity.Radius) {
				w.Runner.Log(fmt.Sprintf("Player (id: %d) and Entity (%f %f) intersects\n", playerMovement.Player.Id, entity.X, entity.Y))
				playerMovement.Player.Health -= PlayerEntityCollisionHealth
				w.Entities[j].Radius -= MaxEntityRadius / 10
			}
		}
		for _, bulletMovement := range w.BulletMovements {
			bulletSegment := Segment{bulletMovement.OldPosition, bulletMovement.Bullet.Position}
			if bulletMovement.Bullet.ShooterId != i && Collides(playerSegment, playerMovement.Player.Tank.Radius(), bulletSegment, bulletMovement.Bullet.Radius) {
				w.Runner.Log(fmt.Sprintf("Player (id: %d) and Bullet (%f %f) intersects\n", playerMovement.Player.Id, bulletMovement.Bullet.X, bulletMovement.Bullet.Y))
				w.Players[bulletMovement.Bullet.ShooterId].Exp += int(bulletMovement.Bullet.Damage * PlayerHitExpCoefficient)
				bulletMovement.Bullet.TTL -= BulletCollisionTTL
				playerMovement.Player.Health -= bulletMovement.Bullet.Damage
			}
		}
		for j, playerMovement2 := range w.PlayerMovements {
			player2Segment := Segment{playerMovement2.OldPosition, playerMovement2.Player.Position}
			if i != j && Collides(playerSegment, playerMovement.Player.Tank.Radius(), player2Segment, playerMovement2.Player.Tank.Radius()) {
				w.Runner.Log(fmt.Sprintf("Player (id: %d) and Player (id: %d) intersects\n", playerMovement.Player.Id, playerMovement2.Player.Id))
				playerMovement.Player.Health -= PlayerPlayerCollisionHealth
			}
		}
	}

	for _, bulletMovement := range w.BulletMovements {
		bulletSegment := Segment{bulletMovement.OldPosition, bulletMovement.Bullet.Position}
		for e, entity := range w.Entities {
			entitySegment := Segment{entity.Position, entity.Position}
			if Collides(bulletSegment, bulletMovement.Bullet.Radius, entitySegment, entity.Radius) {
				w.Runner.Log(fmt.Sprintf("Bullet (%f %f) and Entity (%f %f) intersects\n", bulletMovement.Bullet.X, bulletMovement.Bullet.Y, entity.X, entity.Y))
				w.Players[bulletMovement.Bullet.ShooterId].Exp += int(bulletMovement.Bullet.Damage * EntityHitExpCoefficient)
				bulletMovement.Bullet.TTL -= BulletCollisionTTL
				w.Entities[e].Radius -= bulletMovement.Bullet.Damage * BulletEntityCollisionRadiusCoefficient
			}
		}
	}

	// despawn small entities
	entities := []Entity{}
	for i := range w.Entities {
		entity := &w.Entities[i]
		if entity.Radius > EntityDespawnRadius {
			entities = append(entities, *entity)
		}
	}
	w.Entities = entities

	w.PlayerMovements = nil
	w.BulletMovements = nil

	data, err := json.Marshal(w)
	if err != nil {
		w.Runner.Log(fmt.Sprintf("could not marshal data for observer: %s", err.Error()))
	}
	w.Runner.ToObserver(string(data))
}
