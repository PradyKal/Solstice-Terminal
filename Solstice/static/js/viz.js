/* Solstice Terminal — Three.js 3D Monte Carlo Visualizations */

const SolsticeViz = {
  scenes: {},
  renderers: {},
  animating: {},

  createScene(containerId, options = {}) {
    const container = document.getElementById(containerId);
    if (!container) return null;
    
    const w = container.clientWidth || 600;
    const h = container.clientHeight || 400;
    
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x06080c);
    scene.fog = new THREE.FogExp2(0x06080c, 0.015);
    
    const camera = new THREE.PerspectiveCamera(50, w / h, 0.1, 100);
    camera.position.set(options.camX || 3, options.camY || 2.5, options.camZ || 5);
    
    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(w, h);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    container.appendChild(renderer.domElement);
    
    const controls = new THREE.OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.08;
    controls.autoRotate = options.autoRotate !== false;
    controls.autoRotateSpeed = options.autoRotateSpeed || 0.5;
    controls.minDistance = 1;
    controls.maxDistance = 20;
    
    const ambient = new THREE.AmbientLight(0x404060, 0.5);
    scene.add(ambient);
    
    const dirLight = new THREE.DirectionalLight(0x06b6d4, 1.2);
    dirLight.position.set(2, 5, 3);
    scene.add(dirLight);
    
    const fillLight = new THREE.DirectionalLight(0xa855f7, 0.4);
    fillLight.position.set(-3, 1, -2);
    scene.add(fillLight);
    
    const gridHelper = new THREE.GridHelper(8, 20, 0x1a2030, 0x1a2030);
    gridHelper.position.y = -1.5;
    scene.add(gridHelper);
    
    const resize = () => {
      const w2 = container.clientWidth;
      const h2 = container.clientHeight;
      if (w2 > 0 && h2 > 0) {
        camera.aspect = w2 / h2;
        camera.updateProjectionMatrix();
        renderer.setSize(w2, h2);
      }
    };
    window.addEventListener('resize', resize);
    
    this.scenes[containerId] = { scene, camera, renderer, controls, container };
    this.renderers[containerId] = renderer;
    this.animate(containerId);
    
    return this.scenes[containerId];
  },
  
  animate(id) {
    if (this.animating[id]) return;
    this.animating[id] = true;
    const loop = () => {
      if (!this.animating[id]) return;
      requestAnimationFrame(loop);
      const s = this.scenes[id];
      if (s) { s.controls.update(); s.renderer.render(s.scene, s.camera); }
    };
    loop();
  },
  
  stop(id) { this.animating[id] = false; },
  
  clear(id) {
    this.stop(id);
    const s = this.scenes[id];
    if (s) {
      while (s.scene.children.length) s.scene.remove(s.scene.children[0]);
      s.renderer.dispose();
      const canvas = s.container.querySelector('canvas');
      if (canvas) canvas.remove();
      delete this.scenes[id];
      delete this.renderers[id];
    }
  },

  renderGBM(containerId, data) {
    this.clear(containerId);
    const s = this.createScene(containerId, { autoRotate: true, autoRotateSpeed: 0.3 });
    if (!s) return;
    const { scene } = s;
    const paths = data.path_sample || [];
    if (!paths.length) return;
    const allVals = paths.flat();
    const minV = Math.min(...allVals), maxV = Math.max(...allVals), range = maxV - minV || 1;
    const horizon = paths[0].length;
    const colors = [new THREE.Color(0x06b6d4), new THREE.Color(0x10b981)];
    paths.forEach(path => {
      const pts = [];
      for (let i = 0; i < path.length; i++) {
        pts.push(new THREE.Vector3(
          (i / horizon - 0.5) * 5,
          ((path[i] - minV) / range - 0.5) * 3,
          (Math.random() - 0.5) * 0.8
        ));
      }
      const geo = new THREE.BufferGeometry().setFromPoints(pts);
      const isUp = path[path.length - 1] > path[0];
      const mat = new THREE.LineBasicMaterial({ color: isUp ? colors[1] : colors[0], transparent: true, opacity: 0.08 + Math.random() * 0.12 });
      scene.add(new THREE.Line(geo, mat));
    });
  },

  renderVolSurface(containerId, spot = 100, atmIv = 0.25) {
    this.clear(containerId);
    const s = this.createScene(containerId, { autoRotate: true, autoRotateSpeed: 0.4 });
    if (!s) return;
    const { scene } = s;
    const strikes = [0.7, 0.8, 0.9, 0.95, 1.0, 1.05, 1.1, 1.2, 1.3];
    const maturities = [7, 30, 60, 90, 180, 365];
    const ws = strikes.length - 1, hs = maturities.length - 1;
    const geo = new THREE.PlaneGeometry(4, 3, ws, hs);
    const pos = geo.attributes.position;
    const colors = [];
    let minIV = Infinity, maxIV = -Infinity;
    const ivs = [];
    for (let j = 0; j <= hs; j++) for (let i = 0; i <= ws; i++) {
      const k = strikes[i], T = maturities[j] / 365;
      const m = Math.log(k), iv = Math.max(0.05, atmIv + 0.18*m*m - 0.04*m + 0.05*Math.sqrt(T));
      ivs.push(iv);
      if (iv < minIV) minIV = iv; if (iv > maxIV) maxIV = iv;
    }
    const r = maxIV - minIV || 1;
    for (let j = 0; j <= hs; j++) for (let i = 0; i <= ws; i++) {
      const idx = j * (ws + 1) + i;
      pos.setZ(idx, (ivs[idx] - minIV) / r * 2);
      const t = (ivs[idx] - minIV) / r;
      const c = new THREE.Color().setHSL(0.55 - t * 0.5, 0.9, 0.5);
      colors.push(c.r, c.g, c.b);
    }
    pos.needsUpdate = true; geo.computeVertexNormals();
    geo.setAttribute('color', new THREE.Float32BufferAttribute(colors, 3));
    const mat = new THREE.MeshStandardMaterial({ vertexColors: true, side: THREE.DoubleSide, metalness: 0.15, roughness: 0.4, emissive: 0x06b6d4, emissiveIntensity: 0.08 });
    const mesh = new THREE.Mesh(geo, mat);
    mesh.rotation.x = -Math.PI / 2.2; mesh.position.y = -0.5;
    scene.add(mesh);
    const wf = new THREE.LineSegments(new THREE.WireframeGeometry(geo), new THREE.LineBasicMaterial({ color: 0x06b6d4, transparent: true, opacity: 0.15 }));
    wf.rotation.copy(mesh.rotation); wf.position.copy(mesh.position);
    scene.add(wf);
  },

  renderDistribution(containerId, mean = 0, std = 1) {
    this.clear(containerId);
    const s = this.createScene(containerId, { autoRotate: true, autoRotateSpeed: 0.3 });
    if (!s) return;
    const { scene } = s;
    const n = 100; const positions = []; const colors = [];
    for (let i = 0; i <= n; i++) {
      const t = i / n, x = (t - 0.5) * 6;
      const y = Math.exp(-0.5 * ((x - mean) / std) ** 2) / (std * Math.sqrt(2 * Math.PI)) * 3;
      for (let w = -0.15; w <= 0.15; w += 0.3) {
        positions.push(x, y, w);
        const c = new THREE.Color().setHSL(0.55 - y / 2 * 0.4, 0.8, 0.5);
        colors.push(c.r, c.g, c.b);
      }
    }
    const geo = new THREE.BufferGeometry();
    geo.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));
    geo.setAttribute('color', new THREE.Float32BufferAttribute(colors, 3));
    const mat = new THREE.MeshBasicMaterial({ vertexColors: true, transparent: true, opacity: 0.8, side: THREE.DoubleSide });
    const mesh = new THREE.Mesh(geo, mat);
    mesh.position.y = -1; scene.add(mesh);
  },

  renderScatter(containerId, points, options = {}) {
    this.clear(containerId);
    const s = this.createScene(containerId, { autoRotate: true, autoRotateSpeed: 0.4 });
    if (!s || !points || !points.length) return;
    const { scene } = s;
    const positions = [], colors = [];
    points.forEach((p, i) => {
      positions.push(p.x * 2, p.y * 2, p.z * 2);
      const c = new THREE.Color().setHSL(i / points.length, 0.85, 0.6);
      colors.push(c.r, c.g, c.b);
    });
    const geo = new THREE.BufferGeometry();
    geo.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));
    geo.setAttribute('color', new THREE.Float32BufferAttribute(colors, 3));
    const mat = new THREE.PointsMaterial({ size: options.size || 0.12, vertexColors: true, sizeAttenuation: true, transparent: true, opacity: 0.9 });
    scene.add(new THREE.Points(geo, mat));
  }
};
