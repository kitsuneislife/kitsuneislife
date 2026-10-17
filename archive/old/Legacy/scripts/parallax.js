const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

camera.position.z = 1;

const textureLoader = new THREE.TextureLoader();
Promise.all([
  textureLoader.loadAsync('./assets/background-upscale.png'),
  textureLoader.loadAsync('./assets/depth-map-vector.png')
]).then(([imageTexture, depthTexture]) => {
  const imageAspect = imageTexture.image.width / imageTexture.image.height;
  const screenAspect = window.innerWidth / window.innerHeight;

  const fovRadians = (camera.fov * Math.PI) / 180;
  const height = 2 * Math.tan(fovRadians / 2) * camera.position.z;
  const width = height * camera.aspect;

  let planeWidth = width;
  let planeHeight = height;

  if (imageAspect > screenAspect) {
    planeWidth = height * imageAspect;
  } else {
    planeHeight = width / imageAspect;
  }

  const geometry = new THREE.PlaneGeometry(planeWidth, planeHeight, 100, 100);
  const material = new THREE.ShaderMaterial({
    uniforms: {
      image: { value: imageTexture },
      depth: { value: depthTexture },
      mouse: { value: new THREE.Vector2(0.5, 0.5) }
    },
    vertexShader: `
      varying vec2 vUv;
      void main() {
        vUv = uv;
        gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
      }
    `,
    fragmentShader: `
      uniform sampler2D image;
      uniform sampler2D depth;
      uniform vec2 mouse;
      varying vec2 vUv;

      void main() {
        float depthVal = texture2D(depth, vUv).r;
        vec2 offset = (mouse - 0.5) * 0.03 * (1.0 - depthVal);
        vec4 color = texture2D(image, vUv + offset);
        gl_FragColor = color;
      }
    `
  });

  const mesh = new THREE.Mesh(geometry, material);
  scene.add(mesh);

  document.addEventListener('mousemove', (e) => {
    material.uniforms.mouse.value.x = e.clientX / window.innerWidth;
    material.uniforms.mouse.value.y = 1 - e.clientY / window.innerHeight;
  });

  window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);

    const newHeight = 2 * Math.tan((camera.fov * Math.PI) / 180 / 2) * camera.position.z;
    const newWidth = newHeight * camera.aspect;

    let newPlaneWidth = newWidth;
    let newPlaneHeight = newHeight;

    if (imageAspect > camera.aspect) {
      newPlaneWidth = newHeight * imageAspect;
    } else {
      newPlaneHeight = newWidth / imageAspect;
    }

    const newGeometry = new THREE.PlaneGeometry(newPlaneWidth, newPlaneHeight, 100, 100);
    mesh.geometry.dispose();
    mesh.geometry = newGeometry;
  });

  function animate() {
    requestAnimationFrame(animate);
    renderer.render(scene, camera);
  }
  animate();
});
