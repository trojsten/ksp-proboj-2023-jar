package main

import (
	"fmt"
	"github.com/trojsten/ksp-proboj/libproboj"
)

// Tick executes one game tick
func (w *World) Tick() {
	for i, player := range w.Players {
		w.Runner.ToPlayer(player.Name, fmt.Sprintf("TICK %d", w.TickNumber), w.DataForPlayer(player))
		resp, data := w.Runner.ReadPlayer(player.Name)
		if resp != libproboj.Ok {
			w.Runner.Log(fmt.Sprintf("bad response while reading player %s: %s", player.Name, resp))
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
				playerMovement.Player.Health -= 1 //TODO constant
			}
		}
		for _, bulletMovement := range w.BulletMovements {
			if intersect(playerMovement.OldPosition, playerMovement.Player.Position, playerMovement.Player.Tank.Radius(),
				bulletMovement.OldPosition, bulletMovement.Bullet.Position, bulletMovement.Bullet.Radius) {
				playerMovement.Player.Health -= bulletMovement.Bullet.Damage
				bulletMovement.Bullet.TTL -= 1 //TODO constant
			}
		}
		for j, playerMovement2 := range w.PlayerMovements {
			if i != j && intersect(playerMovement.OldPosition, playerMovement.Player.Position, playerMovement.Player.Tank.Radius(),
				playerMovement2.OldPosition, playerMovement2.Player.Position, playerMovement2.Player.Tank.Radius()) {
				playerMovement.Player.Health -= 1 //TODO constant
			}
		}
	}
}
