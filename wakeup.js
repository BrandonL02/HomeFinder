const puppeteer = require('puppeteer');
const fs = require('fs');

(async () => {
  console.log('💤 Checking if app needs waking up...');

  const browser = await puppeteer.launch({ headless: false, slowMo: 50 });
  const page = await browser.newPage();

  await page.goto('https://homefinder-tampa.streamlit.app/', {
    waitUntil: 'networkidle2',
    timeout: 0,
  });

  await page.waitForTimeout(8000); // Wait for Streamlit to finish animations

  const selector = 'button[data-testid="wakeup-button-owner"]';

  const saveDebug = async () => {
    await page.screenshot({ path: 'debug.png', fullPage: true });
    const html = await page.content();
    fs.writeFileSync('debug.html', html);
    console.log('📝 Saved debug.png and debug.html');
  };

  try {
    // Ensure element is in the DOM
    await page.waitForSelector(selector, { timeout: 10000, visible: true });

    // Scroll into view and click via JS
    const clicked = await page.evaluate((sel) => {
      const btn = document.querySelector(sel);
      if (btn) {
        btn.scrollIntoView();
        btn.click(); // Trigger native click
        return true;
      }
      return false;
    }, selector);

    if (clicked) {
      console.log('✅ Button found and clicked via JS!');
    } else {
      console.log('❌ Button not found or not clickable.');
    }

    await saveDebug();
  } catch (error) {
    console.error('❌ Error during button click:', error.message);
    await saveDebug();
  }

  await browser.close();
})();
