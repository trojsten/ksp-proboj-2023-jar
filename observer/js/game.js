class Game {
    /**
     * @param {Renderer} renderer
     */
    constructor(renderer) {
        /** @type {number} */
        this.frame = 0
        /** @type {Renderer} */
        this.renderer = renderer
        /** @type {Frame[]} */
        this.frames = []
    }

    /** @type {string} observerString */
    loadString(observerString) {
        let lines = observerString.split("\n")
        this.frames = []
        for (let i = 0; i < lines.length; i++) {
            if (!lines[i]) {
                continue
            }
            this.frames.push(JSON.parse(lines[i]))
        }
        this.frame = 0
        this.nextFrame()
    }

    loadGzip(data) {
        let log = new Uint8Array(data)
        try {
            log = pako.inflate(log)
            log = new TextDecoder().decode(log)
        } catch (err) {
            alert("error while inflating: " + err)
        }
        this.loadString(log)
    }

    /** @type {string} url */
    loadUrl(url) {
        fetch(url)
            .then(res => res.blob())
            .then(blob => blob.arrayBuffer())
            .then(data => this.loadGzip(data))
    }

    loadFile(form) {
        form.files[0].arrayBuffer().then(data => {
            this.loadGzip(data)
            this.play()
        })
    }

    nextFrame() {
        this.renderer.render(this.frames[this.frame])
        this.frame++
    }

    play() {
        if (this.frame < this.frames.length) {
            this.nextFrame()
            setTimeout(() => this.play(), this.renderer.frameSpeed)
        }
    }
}