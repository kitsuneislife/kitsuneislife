// audio-player.js by june @ webcatz.neocities.org

/*

how to use:

1. make a new javascript file (ending with .js) somewhere on your site

2. copy this script into it

3. use the script! here's an example setup:

<div id="title">track title</div>
<div id="play">play</div>
<div id="skip">skip</div>

<script src="wherever/youre/storing/audio-player.js"></script>
<script>
AudioPlayer.create([
  // playlist
  {title: "track 1", src: "https://files.catbox.moe/xl09z8.mp3"},
  {title: "track 2", src: "https://files.catbox.moe/xl09z8.mp3"},
  {title: "track 3", src: "https://files.catbox.moe/xl09z8.mp3"},
],{
  // settings
  playButton: document.getElementById("play"),
  skipButton: document.getElementById("skip"),
  title: document.getElementById("title"),
  shuffle: true,
});
</script>

---

want more? here's a list of all possible settings. each one is optional!
  playButton
    any html element. will play/pause the audio when clicked
  skipButton
    any html element. will that will skip the current track when clicked
  title
    any html element. will display the title of the current track
  slider
    any html element except an <input>. will change the current time in the track when dragged
  sliderThumb
    any html element inside the slider. its margin-left will change according to the current time in the track
    has no effect if slider is not set
  sliderProgress
    any html element inside the slider. its width will change according to the current time in the track
    has no effect if slider is not set
  insertIcons
    true or false. if true, inserts icons into the play and skip buttons. false by default
  shuffle
    true or false. if true, shuffles the playlist randomly. false by default
  fileGarden
    a string. instead of passing individual srcs, automatically grabs filegarden srcs. only use if you have a filegarden account.
    set this to the string that appears between "file.garden/" and the next "/" in your files' links.
    instead of an array of objects, use an array of strings as your playlist. these strings should match the names of files in your filegarden's root folder (minus the extension).
  onended
    a function that will run every time a track ends. for adding your own functionality

adding your own functionality? AudioPlayer is just an Audio object with some extra properties:
  list
    an array of objects representing the playlist
  idx
    the current index in the playlist
  next()
    ends the current track and starts the next

*/

const AudioPlayer = new Audio;
AudioPlayer.next = function () {this.dispatchEvent(new Event("ended"))}
AudioPlayer.create = function (list, opts) {
  this.idx = -1;
  this.list = list;

  this.addEventListener("ended", () => {
    this.idx = (this.idx + 1) % this.list.length;
    this.src = this.list[this.idx].src;
  });

  // play button
  if (opts.playButton) {

    opts.playButton.ariaLabel = "play";
    opts.playButton.addEventListener("click", () => this.paused ? this.play() : this.pause());

    if (opts.insertIcons) {

      this.playButton = opts.playButton;
      this.playIcon = '<i class="fa-solid fa-play"></i>';
      this.loadIcon = "<svg fill=\"currentcolor\" width=\"1em\" height=\"1em\" style=\"vertical-align: -0.125em; pointer-events: none\" viewBox=\"0 0 512 512\" aria-hidden=\"true\"><!--!Font Awesome Free 6.5.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2024 Fonticons, Inc.--><path d=\"M304 48a48 48 0 1 0 -96 0 48 48 0 1 0 96 0zm0 416a48 48 0 1 0 -96 0 48 48 0 1 0 96 0zM48 304a48 48 0 1 0 0-96 48 48 0 1 0 0 96zm464-48a48 48 0 1 0 -96 0 48 48 0 1 0 96 0zM142.9 437A48 48 0 1 0 75 369.1 48 48 0 1 0 142.9 437zm0-294.2A48 48 0 1 0 75 75a48 48 0 1 0 67.9 67.9zM369.1 437A48 48 0 1 0 437 369.1 48 48 0 1 0 369.1 437z\"/></svg>";
      this.pauseIcon = '<i class="fa-solid fa-pause"></i>';

      this.playButton.ariaLabel = "play";
      this.playButton.innerHTML = this.playIcon;

      this.addEventListener("play", () => {
        this.playButton.ariaLabel = "pause";
        this.playButton.innerHTML = this.loadIcon;
        this.addEventListener("timeupdate", () => this.playButton.innerHTML = this.pauseIcon, {once: true});
      });
      this.addEventListener("pause", () => {
        this.playButton.ariaLabel = "play";
        this.playButton.innerHTML = this.playIcon;
      });

    }
  }

  // skip button
  if (opts.skipButton) {
    opts.skipButton.ariaLabel = "skip";
    opts.skipButton.addEventListener("click", () => this.next());
    if (opts.insertIcons) opts.skipButton.innerHTML = '<i class="fa-solid fa-forward"></i>';
  }

  // title
  if (opts.title) {
    this.titleEl = opts.title;
    this.addEventListener("ended", () => this.titleEl.textContent = this.list[this.idx].title);
  }

  // custom slider
  if (opts.slider) {
    this.slider = opts.slider;
    this.slider.role = "slider";
    this.slider.ariaValueMin = 0;
    this.slider.tabIndex = 0;

    this.dispatchSliderEvent = percent => this.slider.dispatchEvent(new CustomEvent("input", {detail: {percent: percent}}));

    // updating max
    this.addEventListener("durationchange", () => {
      this.slider.ariaValueMax = this.duration;
    })
    // updating value
    this.addEventListener("timeupdate", () => {
      this.slider.ariaValueNow = this.currentTime;
      this.dispatchSliderEvent(this.currentTime / this.duration);
    });

    // mouse events
    this.slider.addEventListener("mousedown", () => {
      this.sliderX = this.slider.getBoundingClientRect().left;
      addEventListener("mousemove", this.sliderMove);
      addEventListener("mouseup", this.sliderUp, {once: true});
    });
    this.sliderMove = e => {
      this.dispatchSliderEvent(Math.max(0, Math.min(this.slider.clientWidth, e.x - this.sliderX)) / this.slider.clientWidth);
    }
    this.sliderUp = e => {
      removeEventListener("mousemove", this.sliderMove);
      this.currentTime = this.duration * Math.max(0, Math.min(this.slider.clientWidth, e.x - this.sliderX)) / this.slider.clientWidth;
      delete this.sliderX;
    }

    // slider thumb
    if (opts.sliderThumb) {
      this.sliderThumb = opts.sliderThumb;
      this.slider.addEventListener("input", e => {
        this.sliderThumb.style.marginLeft = (this.slider.clientWidth - this.sliderThumb.clientWidth) * e.detail.percent + "px";
      });
    }
    // slider progress
    if (opts.sliderProgress) {
      this.sliderProgress = opts.sliderProgress;
      this.slider.addEventListener("input", e => {
        this.sliderProgress.style.width = this.slider.clientWidth * e.detail.percent + "px";
      });
    }
  }

  // shuffling playlist
  if (opts.shuffle) {
    let thisi = this.list.length, randi;
    while (thisi > 0) randi = Math.floor(Math.random() * thisi--), [this.list[thisi], this.list[randi]] = [this.list[randi], this.list[thisi]];
  }

  // file.garden srcs
  if (opts.fileGarden) {
    this.list = this.list.map(track => track = {title: track, src: "https://file.garden/" + opts.fileGarden + "/" + encodeURIComponent(track) + ".mp3"});
  }

  // ended
  if (opts.onended) this.addEventListener("ended", opts.onended);

  this.next();
  this.addEventListener("ended", this.play);
}