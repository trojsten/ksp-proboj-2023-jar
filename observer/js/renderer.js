/**
 * @typedef Player
 * @prop {number} id
 * @prop {string} name
 * @prop {number} x
 * @prop {number} y
 * @prop {number} angle
 * @prop {boolean} alive
 * @prop {number} tank_id
 * @prop {number} tank_radius
 */

/**
 * @typedef Position
 * @prop {number} x
 * @prop {number} y
 */

/**
 * @typedef Bullet
 * @prop {number} id
 * @prop {number} radius
 * @prop {Position} position
 * @prop {number} shooter_id
 */

/**
 * @typedef Entity
 * @prop {number} radius
 * @prop {Position} position
 */

/**
 * @typedef Frame
 * @prop {Player[]} players
 * @prop {Bullet[]} bullets
 * @prop {Entity[]} entities
 * @prop {number} size
 * @prop {number} tick_number
 */

class Renderer {
    constructor() {
        this.app = new PIXI.Application({ background: '#111', resizeTo: document.body, antialias: true })
        document.body.appendChild(this.app.view)

        /** @type {Object.<number, _Graphics>}} */
        this.worldPlayers = {}
        /** @type {Object.<number, _Graphics>}} */
        this.worldBullets = {}
        /** @type {_Graphics} */
        this.worldBorder = null
        /** @type {number} */
        this.frameSpeed = 100

        /** @type {_Container} */
        this.entityLayer = null

        /** @type {_Container} */
        this.world = new PIXI.Container()
        this.app.stage.addChild(this.world)
        this.app.ticker.add(() => TWEEDLE.Group.shared.update())
        this.app.ticker.add(() => this.recenter())
        // this.world.x = this.app.screen.width / 2
        // this.world.y = this.app.screen.height / 2
        // this.world.scale.x = 0.5
        // this.world.scale.y = 0.5
    }

    /**
     * @param {Frame} frame
     */
    render(frame) {
        this.renderBorder(frame.size)

        // Players
        for (const player of frame.players) {
            if (!player.alive) {
                if (player.id in this.worldPlayers) {
                    this.world.removeChild(this.worldPlayers[player.id])
                    delete this.worldPlayers[player.id]
                }
                continue
            }

            this.renderPlayer(player)
        }

        // Bullets
        let currentBullets = new Set()
        for (const bullet of frame.bullets) {
            currentBullets.add(bullet.id)
            this.renderBullet(bullet)
        }

        for (const i of Object.keys(this.worldBullets)) {
            if (!currentBullets.has(parseInt(i))) {
                this.world.removeChild(this.worldBullets[i])
                delete this.worldBullets[i]
            }
        }

        // Entities
        if (this.entityLayer) {
            this.world.removeChild(this.entityLayer)
        }
        this.entityLayer = new PIXI.Container()
        this.world.addChildAt(this.entityLayer, 1)
        for (const entity of frame.entities) {
            this.renderEntity(entity)
        }
    }

    recenter() {
        const keys = Object.keys(this.worldPlayers)
        if (keys.length === 0) {
            return
        }
        let minX, minY, maxX, maxY;
        const key = parseInt(keys[0])
        minX = maxX = this.worldPlayers[key].x
        minY = maxY = this.worldPlayers[key].y

        for (const player of Object.values(this.worldPlayers)) {
            minX = Math.min(minX, player.x)
            maxX = Math.max(maxX, player.x)
            minY = Math.min(minY, player.y)
            maxY = Math.max(maxY, player.y)
        }

        const boxWidth = maxX - minX + 100
        const boxHeight = maxY - minY + 100

        const zoom = Math.min(this.app.screen.width / boxWidth, this.app.screen.height / boxHeight)
        const centerX = (maxX + minX) / 2
        const centerY = (maxY + minY) / 2
        this._tween(this.world, {
            x: this.app.screen.width / 2 - centerX * zoom,
            y: this.app.screen.height / 2 - centerY * zoom,
            scale: {
                x: zoom,
                y: zoom,
            }
        })
    }

    /**
     * @param {Player} player
     */
    renderPlayer(player) {
        if (!(player.id in this.worldPlayers)) {
            const g = new PIXI.Graphics()
            const color = playerColor(player.id)

            g.lineStyle(2, 0xFFFFFF, 1)
            g.beginFill(color, 1)
            g.drawCircle(0, 0, 10)
            g.endFill();

            g.lineStyle(2, 0xffd900, 1)
            g.moveTo(0, 0)
            g.lineTo(0, -20)
            g.closePath()
            g.x = player.x
            g.y = -player.y
            g.rotation = player.angle

            this.worldPlayers[player.id] = g
            this.world.addChild(g)
        }

        const wp = this.worldPlayers[player.id]
        this._tween(wp, {
            x: player.x,
            y: -player.y,
            rotation: player.angle
        })
    }

    /**
     * @param {Bullet} bullet
     */
    renderBullet(bullet) {
        if (!(bullet.id in this.worldBullets)) {
            const b = new PIXI.Graphics();
            b.beginFill(playerColor(bullet.shooter_id), 1);
            b.drawCircle(0, 0, bullet.radius);
            b.endFill();
            b.x = bullet.position.x
            b.y = -bullet.position.y
            this.worldBullets[bullet.id] = b
            this.world.addChildAt(b, 1)
        }

        const wb = this.worldBullets[bullet.id]
        this._tween(wb, {
            x: bullet.position.x,
            y: -bullet.position.y,
        })
    }

    /**
     * @param {number} size
     */
    renderBorder(size) {
        if (this.worldBorder) {
            this.world.removeChild(this.worldBorder)
        }

        const g = new PIXI.Graphics()
        g.lineStyle(1, 0xffffff, 0.8)
        g.beginFill(0xffffff, 0.1)
        g.moveTo(-size, -size)
        g.lineTo(size, -size)
        g.lineTo(size, size)
        g.lineTo(-size, size)
        g.closePath()
        this.worldBorder = g
        this.world.addChildAt(g, 0)
    }

    /** @type {Entity} entity */
    renderEntity(entity) {
        const b = new PIXI.Graphics();
        b.beginFill(0xffee00, 1);
        b.drawCircle(0, 0, entity.radius);
        b.endFill();
        b.x = entity.position.x
        b.y = -entity.position.y
        this.entityLayer.addChild(b)
    }

    _tween(obj, to) {
        new TWEEDLE.Tween(obj).to(to, this.frameSpeed).start()
    }
}
