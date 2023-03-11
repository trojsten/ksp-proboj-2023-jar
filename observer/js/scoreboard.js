

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

    /**
     * @param {Player} player
     * @private
     * @return {_Container}
     */
    _createPlayer(player) {
        const c = new PIXI.Container()

        const g = new PIXI.Graphics()
        g.beginFill(0x333333)
        g.moveTo(0, 0)
        g.lineTo(200, 0)
        g.lineTo(200, 30)
        g.lineTo(0, 30)
        g.endFill()

        g.beginFill(playerColor(player.id))
        g.moveTo(5, 5)
        g.lineTo(25, 5)
        g.lineTo(25, 25)
        g.lineTo(5, 25)
        g.endFill()
        c.addChild(g)

        const name = new PIXI.Text(player.name, {
            fontSize: 15,
            fontWeight: "bold",
            fill: "#fff",
        })
        name.x = 30
        name.y = 15
        name.anchor.set(0, 0.5)
        c.addChild(name)

        // todo: show real score
        const score = new PIXI.Text("0", {
            fontSize: 15,
            fontWeight: "bold",
            fill: "#fff",
            align: "right",
        })
        score.x = 195
        score.y = 15
        score.anchor.set(1, 0.5)
        score.name = "score"
        c.addChild(score)

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
                const c = this._createPlayer(player)
                this.players[player.name] = c
                this.container.addChild(c)
            }
        }

        for (const key in this.players) {
            if (!current.has(key)) {
                this.container.removeChild(this.players[key])
                this.players[key].destroy()
                delete this.players[key]
            }
        }

        // todo: sort players by score
        const sorted = Object.keys(this.players)
        for (let i = 0; i < sorted.length; i++) {
            new TWEEDLE.Tween(this.players[sorted[i]]).to({
                y: i*32,
            }, frameSpeed).start()
        }
    }

}
