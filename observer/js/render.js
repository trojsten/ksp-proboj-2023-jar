let worldPlayers = {}
let worldBullets = {}

const TESTFrame = {
    players: [
        {
            x: 1.34,
            y: 3.2,
            angle: 23,
            alive: true,
            id: 1,
            name: "hrac",
            tank_id: 1,
            tank_radius: 10,
        }
    ],
    bullets: [
        {
            position: {
                x: 20.34,
                y: 13.2,
            },
            id: 1,
            shooter_id: 1,
            radius: 3,
        },
    ],
}
function renderFrame(frame) {
    for (const player of frame.players) {
        if (!player.alive) {
             if (player.id in worldPlayers) {
                 world.removeChild(worldPlayers[player.id])
                 delete worldPlayers[player.id]
             }
            continue
        }

        if (!(player.id in worldPlayers)) {
            let p = newPlayer()
            worldPlayers[player.id] = p
            world.addChild(p)
        }
        let wp = worldPlayers[player.id]
        wp.x = player.x
        wp.y = -player.y
        wp.rotation = player.angle
    }

    let currentBullets = new Set()
    for (const bullet of frame.bullets) {
        currentBullets.add(bullet.id)
        if (!(bullet.id in worldBullets)) {
            let b = newBullet(bullet.radius)
            worldBullets[bullet.id] = b
            world.addChild(b)
        }
        let wb = worldBullets[bullet.id]
        wb.x = bullet.position.x
        wb.y = -bullet.position.y
    }

    for (const i of Object.keys(worldBullets)) {
        if (!currentBullets.has(parseInt(i))) {
            world.removeChild(worldBullets[i])
            delete worldBullets[i]
        }
    }
}
