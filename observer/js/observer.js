const renderer = new Renderer()
const game = new Game(renderer);
// game.loadUrl("observer.dat")

document.getElementById("js-speed").addEventListener("change", (e) => {
    game.renderer.frameSpeed = parseInt(e.target.value)
})

document.getElementById("js-slider").addEventListener("input", (e) => {
    game.nextFrameId = parseInt(e.target.value)
})

document.getElementById("js-play").addEventListener("click", (e) => {
    game.startPlayback()
})

document.getElementById("js-pause").addEventListener("click", (e) => {
    game.stopPlayback()
})

document.addEventListener("keydown", (e) => {
    if (e.code === "Space") {
        if (game.playing) {
            game.stopPlayback()
        } else {
            game.startPlayback()
        }
        e.preventDefault()
    }
})
