document.addEventListener('DOMContentLoaded', () => {

    const video = document.getElementById('video-background');

    // A 'força' do efeito. Valores maiores = movimento mais intenso.
    const parallaxStrength = 0.03;

    // Adiciona um "ouvinte" para o evento de movimento do mouse na janela inteira
    window.addEventListener('mousemove', (event) => {
        // Pega a posição X e Y do mouse
        const { clientX, clientY } = event;

        // Calcula o centro da tela
        const centerX = window.innerWidth / 2;
        const centerY = window.innerHeight / 2;

        // Calcula a diferença entre a posição do mouse e o centro
        const moveX = (clientX - centerX) * parallaxStrength;
        const moveY = (clientY - centerY) * parallaxStrength;

        // Aplica o movimento ao vídeo usando a propriedade 'transform' do CSS.
        // É importante manter o 'scale' inicial e adicionar o 'translate'.
        video.style.transform = `translateX(-50%) translateY(-50%) scale(1.1) translate(${moveX}px, ${moveY}px)`;
    });

});