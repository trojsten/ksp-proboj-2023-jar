const app = new PIXI.Application({ background: '#111', resizeTo: document.body, antialias: true });
document.body.appendChild(app.view);

const world = new PIXI.Container();
app.stage.addChild(world);

function newPlayer() {
    const g = new PIXI.Graphics();
    g.lineStyle(2, 0xeeeeee, 1);
    g.beginFill(0xC34288, 1);
    g.drawCircle(0, 0, 10);
    g.endFill();

    g.lineStyle(2, 0xffd900, 1);
    g.moveTo(0, 0);
    g.lineTo(0, -20);
    g.closePath();
    return g;
}

function newBullet(radius) {
    const g = new PIXI.Graphics();
    g.beginFill(0xC34288, 1);
    g.drawCircle(0, 0, radius);
    g.endFill();
    return g;
}

world.x = app.screen.width / 2;
world.y = app.screen.height / 2;
