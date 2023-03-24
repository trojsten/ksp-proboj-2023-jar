function render_tank(g, color, player) {
    g.lineStyle(2, 0xFFFFFF, 1)
    g.beginFill(color, 1)
    g.drawCircle(0, 0, player.tank_radius)
    g.endFill();
    
    switch (player.tank_id){
        
        case 0: { // BasicTank
            render_basic_shaft(g, 2, 20)
            break
        }
        case 1: {
            render_basic_shaft(g, 1, 15, -2)
            render_basic_shaft(g, 1, 15, +2)
            break
        }
        case 2: { // EverywhereTank
            g.lineStyle(2, 0xffd900, 1)
            for(let i=0; i<8; i++) {
                g.moveTo(0, 0)
                g.lineTo(-15*Math.sin(2*i*Math.PI), -15*Math.cos(2*i*Math.PI))
                g.closePath()
            }
            break
        }
        case 3: {
            render_basic_shaft(g, 1, +15)
            g.lineStyle(2, 0xffd900, 1)
            g.moveTo(0, 0)
            g.lineTo(-15*Math.sin(Math.PI/2), -15*Math.cos(Math.PI/2))
            g.closePath()
            break
        }
        case 4: { // DoubleDoubleTank
            render_basic_shaft(g, 1, +15, -2)
            render_basic_shaft(g, 1, +15, +2)
            render_basic_shaft(g, 1, -15, -2)
            render_basic_shaft(g, 1, -15, +2)
            break
        }
        case 5: { // SniperTank
            render_basic_shaft(g, 2, 40)
            break
        }
        case 6: { // WideBulletTank
            render_basic_shaft(g, 5, 20)
            break
        }
        case 7: { // GuidedBulletTank
            render_basic_shaft(g, 2, 50)
            break
        }
        case 8: { // MachineGunTank
            for(let i=-3; i<=3; i++)
                render_basic_shaft(g, 1, 15, i)
            break
        }
        case 9: { // AsymetricTank
            render_basic_shaft(g, 1, 15)
            render_basic_shaft(g, 1, -5)
            break
        }
        case 10: { // PeacefulTank
            break
        }
        case 11: { // InvisibleBulletTank
            render_basic_shaft(g, 8, 20)
            break
        }
        case 12: {  // SymetricTripleTank
            render_basic_shaft(g, 2, 20)

            g.lineStyle(2, 0xffd900, 1)
            g.moveTo(0, 0)
            g.lineTo(-10*Math.sin(+2*Math.PI/3), -10*Math.cos(+2*Math.PI/3))
            g.closePath()


            g.moveTo(0, 0)
            g.lineTo(-10*Math.sin(-2*Math.PI/3), -10*Math.cos(-2*Math.PI/3))
            g.closePath()
            break
        }
    }
}

function render_basic_shaft(g, width, length, offset=0) {
    g.lineStyle(width, 0xffd900, 1)
    g.moveTo(offset, 0)
    g.lineTo(offset, -1*length)
    g.closePath()
}
