class Scoreboard {
    /**
     * @param {_Container} container
     */
    constructor(container) {
        /** @type _Container */
        this.container = container
        /** @type Object.<string,_Container> */
        this.players = {}
    }

    width = 300
    height = 30
    topHeight = 20
    gap = 2

    tankTypes = {
            0: 'Basic',
            1: 'Twin',
            2: 'Everywhere',
            3: 'GuidedBullet',
            4: 'DoubleDouble',
            5: 'Sniper',
            6: 'WideBullet',
            7: 'GuidedBullet',
            8: 'MachineGun',
            9: 'Asymetric',
            10: 'Peaceful',
            11: 'InvisibleBullet',
            12: 'SymetricTriple'
    }

    /**
     * @param {Player} player
     * @private
     * @return {_Container}
     */
    _createPlayer(player) {
        const c = new PIXI.Container()

        const g = new PIXI.Graphics()
        g.beginFill(player.alive ? 0x333333 : 0x222222)
        g.moveTo(0, 0)
        g.lineTo(this.width, 0)
        g.lineTo(this.width, this.height)
        g.lineTo(0, this.height)
        g.endFill()
        c.addChild(g)

        const text_color = player.alive ? '#fff' : '#aaa'

        const tank = new PIXI.Graphics()
        render_tank(tank, player.alive ? playerColor(player.id) : 0xeeeeee, player)
        tank.x = this.topHeight / 2
        tank.y = this.topHeight / 2
        tank.rotation = Math.PI / 4
        c.addChild(tank)

        const name = new PIXI.Text(player.name, {
            fontSize: 14,
            fontWeight: "bold",
            fill: text_color,
        })
        name.x = 30
        name.y = Math.floor(this.topHeight / 2 - name.height / 2)
        name.anchor.set(0, 0)
        c.addChild(name)

        const type = new PIXI.Text(this.tankTypes[player.tank_id], {
                fontSize: 12,
                fontWeight: "normal",
                fill: text_color,
        })

        type.x = this.width - 75
        type.y = Math.floor(this.topHeight / 2 - type.height / 2)
        type.anchor.set(1, 0)
        c.addChild(type)

        const score = new PIXI.Text(`${player.score}`, {
            fontSize: 14,
            fontWeight: "bold",
            fill: text_color,
            align: "right",
        })
        score.x = this.width - 5
        score.y = Math.floor(this.topHeight / 2 - name.height / 2)
        score.anchor.set(1, 0)
        score.name = "score"
        c.addChild(score)

        const stats = new PIXI.Text(`R: ${player.stats.range} | S: ${player.stats.speed} ` +
            `| Bs: ${player.stats.bullet_speed} | Bt: ${player.stats.bullet_ttl} ` +
            `| Bd: ${player.stats.bullet_damage} | H: ${player.stats.health_max} | Rg: ${player.stats.health_regeneration} ` +
            `| D: ${player.stats.body_damage} | Rl: ${player.stats.reload_speed}`, {
            fontSize: 10,
            fill: text_color,
        })
        stats.x = 5
        stats.y = this.topHeight - 1
        // stats.y = Math.floor(this.topHeight / 2 - name.height / 2)
        stats.anchor.set(0, 0)
        c.addChild(stats)

        return c
    }

    /**
     * @param {Player[]} players
     * @param {number} frameSpeed
     */
    render(players, frameSpeed) {
        let current = new Set()
        for (const player of players) {
            current.add(player.name)

            if (!(player.name in this.players)) {
                const outer = new PIXI.Container()
                this.players[player.name] = outer
                this.container.addChild(outer)
            }

            const p = this.players[player.name]
            const c = this._createPlayer(player)
            for (const ch of p.removeChildren()) {
                ch.destroy(true)
            }
            p.addChild(c)
        }

        for (const key in this.players) {
            if (!current.has(key)) {
                this.container.removeChild(this.players[key])
                this.players[key].destroy(true)
                delete this.players[key]
            }
        }

        const scores = {}
        for (const p of players) {
            scores[p.name] = p.score
        }
        
        const sorted = Object.keys(this.players).sort((a, b) => scores[b] - scores[a])
        for (let i = 0; i < sorted.length; i++) {
            new TWEEDLE.Tween(this.players[sorted[i]]).to({
                y: i * (this.height + this.gap),
            }, frameSpeed).start()
        }
    }

}
