
const audioEls = document.getElementById("audio-player").children;
var nightcore = false;
AudioPlayer.create([
  "First Steps - Lena Raine (Celeste OST)",
  "Forgo's Treasures - Hirokazu Ando (Kirby and the Forgotten Land OST)",
  "Allison's Theme - beatrix quinn (Super Lesbian Animal RPG OST)",
  "Dark Flute - Jim Guthrie (Sword & Sworcery LP - The Ballad of the Space Babies)",
  "Paramnesiac - still crisp (Pseudoregalia OST)",
  "Marine Tube - Go Ichinose (Pokémon Black & White 2 OST)",
  "Relic - Aaron Cherof (Minecraft: Trails & Tales OST)",
  "Eliezer's Waltz - Disparition (Welcome to Night Vale)",
  "I Feel Like (Live) - coffeebug (MIDIfreak)",
  "See You At The Top - Mark Sparling (A Short Hike OST)",
  "pawprints in the snow - coffeebug (haunted sticky notes)",
  "Strange Quest - Joel Corelitz (Eastward OST)",
],{
  playButton: audioEls[3],
  skipButton: audioEls[5],
  insertIcons: true,
  slider: audioEls[4],
  sliderThumb: audioEls[4].children[2],
  sliderProgress: audioEls[4].children[1],
  shuffle: true,
  fileGarden: "ZdmFgugxzVCR-8Bl",
  onended: () => {
    let newTitle = document.createElement("marquee");
    newTitle.textContent = AudioPlayer.list[AudioPlayer.idx].title, newTitle.className = "lcd", newTitle.scrollAmount = 4;
    audioEls[1].replaceWith(newTitle);
    audioEls[0].textContent = AudioPlayer.idx + 1 + "/" + AudioPlayer.list.length;
    if (lightsOff) AudioPlayer.playbackRate = 0.6;
    else if (nightcore) AudioPlayer.playbackRate = 1.5;
  }
});
AudioPlayer.addEventListener("durationchange", () => audioEls[2].innerText = Math.floor(AudioPlayer.duration / 60) + ":" + ("0" + Math.round(AudioPlayer.duration % 60)).slice(-2));

AudioPlayer.preservesPitch = false, AudioPlayer.webkitPreservesPitch = false;
document.getElementById("awful-fucking-thing").onclick = () => {
  if (nightcore = !nightcore) {
    document.getElementById("audio-player").classList.add("nightcore");
    document.getElementById("awful-fucking-thing").firstChild.src = "/Assets/awful-fucking-thing-2.webp";
    AudioPlayer.playbackRate = 1.5;
  } else {
    document.getElementById("audio-player").classList.remove("nightcore");
    document.getElementById("awful-fucking-thing").firstChild.src = "/Assets/awful-fucking-thing.webp";
    AudioPlayer.playbackRate = 1;
  }
}

/*document.getElementById("track-name").textContent = tracklist[0].name;
document.getElementById("tunes").querySelector("iframe").src = getURL(tracklist[0].hash);
tracklist = null;*/

var lightsOff = false;
document.getElementById("lightswitch").onclick = function () {
  new Audio("https://files.catbox.moe/as06cd.mp3").play();
  lightsOff = !lightsOff;
  if (lightsOff) {
    document.body.classList.add("lights-off");
    AudioPlayer.playbackRate = 0.6;
  } else {
    document.body.classList.remove("lights-off");
    AudioPlayer.playbackRate = nightcore ? 1.5 : 1;
  }
}

const starWrapper = document.body.appendChild(document.createElement("div"));
starWrapper.id = "star-wrapper", starWrapper.ariaHidden = true;
const colors = ["var(--blue)", "var(--red)", "var(--yellow)"];
const starMaxX = innerWidth - 7, starMaxY = innerHeight - 7;
let expCount = 0;

onclick = e => {
  if (expCount <= 5) {
    let colori = Math.floor(Math.random() * 3 * colors.length), intensity = 5 + Math.random() * 4;
    let stars = [];
    expCount++;
    for (let i = 0; i < 75; i++) {
      stars[i] = {
        el: document.createElement('div'),
        x: e.pageX, y: e.pageY - 5,
        dX: (Math.random() - 0.5) * 1.25,
        dY: (Math.random() - 0.5) * intensity,
        decay: Math.floor(Math.random() * 16) + 16,
        intensity: intensity,
      };
      stars[i].dX *= intensity - Math.abs(stars[i].dY);
      stars[i].el.className = "star";
      if (colori < colors.length) stars[i].el.style.color = colors[i % 2 ? expCount % colors.length : colori];
      else if (colori < 2 * colors.length) stars[i].el.style.color = colors[expCount % colors.length];
      else stars[i].el.style.color = colors[i % colors.length];
      stars[i].el.ariaHidden = true;
      stars[i].el.append("*");
      starWrapper.appendChild(stars[i].el);
    }
    explode(stars);
  }
}

async function explode(stars) {
  let starCount = 75;
  do {
    for (const star of stars) if (star.decay) {
      star.dY += 1.25 / star.intensity, star.x += star.dX, star.y += star.dY;
      star.el.style.left = star.x + 'px', star.el.style.top = star.y + 'px';
      switch (--star.decay) {
        case 14: star.el.style.fontSize = '7px'; break;
        case 6: star.el.style.fontSize = '2px'; break;
        case 0: star.el.remove(); starCount--;
      }
    }
    await wait(33);
  } while (starCount);
  expCount--;

  function wait(ms) {return new Promise(resolve => setTimeout(resolve, ms))}
}