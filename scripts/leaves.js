const container = document.getElementById('leaf-container');

function createLeaf() {
const leaf = document.createElement('div');
leaf.className = 'leaf';

const size = Math.random() * 10 + 20;
leaf.style.width = `${size}px`;
leaf.style.height = `${size}px`;

let x = Math.random() * window.innerWidth;
let y = -size;

const rotateSpeed = Math.random() * 0.1 + 1;
const swayAmplitude = Math.random() * 30 + 20;
const swayFrequency = Math.random() * 0.01 + 0.005;
const fallSpeed = Math.random() * 1.5 + 0.5;
const windSpeed = Math.random() * -1.5 - 0.5; // Vento indo para a esquerda

let angle = Math.random() * 360;

container.appendChild(leaf);

function animate() {
    y += fallSpeed;
    x += windSpeed + Math.sin(y * swayFrequency) * swayAmplitude * 0.01;
    angle += rotateSpeed;

    leaf.style.transform = `translate(${x}px, ${y}px) rotate(${angle}deg)`;

    if (y < window.innerHeight + size && x > -size) {
    requestAnimationFrame(animate);
    } else {
    leaf.remove();
    }
}

animate();
}

setInterval(createLeaf, 2500);

