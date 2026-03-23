// Evervault-style Interactive Canvas

  // Cards Data
  const cardData = [
    {
      name: "ELON MUSK",
      logo: "Elon Musk",
      number: "1234 5678 9000 0000",
      expiry: "12/28",
      image: "https://images.unsplash.com/photo-1614850523459-c2f4c699c52e?w=800&q=80",
      type: "elon"
    },
    {
      name: "STEVE JOBS",
      logo: "AAPL",
      number: "5555 4444 3333 2222",
      expiry: "09/30",
      image: "https://images.unsplash.com/photo-1557682250-33bd709cbe85?w=800&q=80",
      type: "aapl"
    },
    {
      name: "STRIPE",
      logo: "stripe",
      number: "4000 1234 5678 9010",
      expiry: "11/25",
      image: "https://images.unsplash.com/photo-1557672172-298e090bd0f1?w=800&q=80",
      type: "stripe"
    }
  ];

  const cardLine = document.getElementById('cardLine');
  const wrapper = document.getElementById('evervaultWrapper');
  const scanner = document.getElementById('scanner');

  // Build Cards Loop to ensure enough cards for infinity
  // Duplicate array
  const fullCards = [...cardData, ...cardData, ...cardData];

  fullCards.forEach((data, index) => {
    // Random ascii string
    const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+{}|:"<>?~`-=[]\\;\',./';
    let asciiStr = '';
    for(let i=0; i<3000; i++) asciiStr += chars[Math.floor(Math.random()*chars.length)];

    const html = `
      <div class="card-wrapper" id="card-${index}">
        <!-- ASCII Card -->
        <div class="card card-ascii">
          <div class="ascii-content">${asciiStr}</div>
        </div>
        <!-- Normal Card -->
        <div class="card card-normal">
          <img class="card-image" src="${data.image}" style="${data.type === 'stripe' ? 'filter: hue-rotate(90deg);' : ''}" />
          <div style="padding:25px; height:100%; display:flex; flex-direction:column; justify-content:space-between; position:relative; z-index:2;">
            <div style="display:flex; justify-content:space-between; width: 100%;">
              ${data.type !== 'stripe' ? '<div class="card-chip"></div>' : '<div style="width:30px;height:30px;"></div>'}
              <div class="card-logo">${data.logo}</div>
            </div>
            <div>
              <div class="card-number">${data.number}</div>
              <div class="card-info">
                <span class="card-holder">${data.name}</span>
                <span class="card-expiry">${data.expiry}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    `;
    cardLine.insertAdjacentHTML('beforeend', html);
  });

  // Animation State Control
  let isPlaying = true;
  let direction = -1; // 1 = right, -1 = left
  let speed = 80;
  let xPos = 0;
  const speedVal = document.getElementById('speedValue');

  window.toggleAnimation = () => { isPlaying = !isPlaying; };
  window.resetPosition = () => { xPos = 0; };
  window.changeDirection = () => { direction *= -1; };

  // Main Loop
  let lastTime = performance.now();
  let wrapperWidth = 0;
  let scannerX = 0;
  
  function updateLayout() {
    if (wrapper) {
      wrapperWidth = wrapper.offsetWidth;
      scannerX = wrapperWidth / 2;
    }
  }
  window.addEventListener('resize', updateLayout);
  updateLayout();

  function animate(time) {
    requestAnimationFrame(animate);
    const delta = (time - lastTime) / 1000;
    lastTime = time;

    // Filter out huge deltas if tab changes
    if (delta > 0.1) return;

    if (!wrapper || !cardLine) return;

    // Scroll stream horizontal
    if (isPlaying) {
      xPos += (speed * direction * delta);
      // Continuous loop logic (loop back when completely out)
      // card width = 400, gap = 60. 3 sets = 9 cards * 460 = 4140px
      const cycleWidth = 3 * 460;
      if (xPos <= -cycleWidth) xPos += cycleWidth;
      if (xPos >= cycleWidth) xPos -= cycleWidth;
      cardLine.style.transform = `translateX(${xPos}px)`;
    }

    // Clip Mask Logic Analytical (NO Layout Thrashing)
    const wrappers = document.querySelectorAll('.card-wrapper');
    wrappers.forEach((cardRow, index) => {
      const cardLeft = xPos + index * 460;
      const xInsideCard = scannerX - cardLeft;
      let percent = (xInsideCard / 400) * 100;
      
      // Boundaries
      percent = Math.max(0, Math.min(100, percent));
      
      cardRow.querySelector('.card-normal').style.setProperty('--clip-right', percent + '%');
      cardRow.querySelector('.card-ascii').style.setProperty('--clip-left', percent + '%');
    });
  }
  requestAnimationFrame(animate);
