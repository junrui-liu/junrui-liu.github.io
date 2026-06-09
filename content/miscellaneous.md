+++
title = "Misc"
menu = "main"
weight = 30
+++

<center>
<span class="bell-wrap"><button class="bell-btn" type="button" aria-label="Bell" onclick="bellClick(this)">🔔</button><span class="bell-msg" aria-live="polite"></span></span>
</center>
<audio id="chime-audio" src="/audio/waltz.mp3" preload="metadata" style="display:none"></audio>
<script>
  function bellClick(btn) {
    const msg = document.querySelector('.bell-msg');
    const audio = document.getElementById('chime-audio');
    const state = btn.dataset.state || 'idle';
    if (state === 'idle') {
      btn.dataset.state = 'primed';
      btn.classList.add('primed');
      msg.textContent = 'ring me!';
    } else if (state === 'primed') {
      btn.dataset.state = 'playing';
      btn.classList.remove('primed');
      btn.classList.add('playing');
      audio.currentTime = 0;
      audio.play();
      msg.textContent = 'click again to shush';
    } else {
      btn.dataset.state = 'idle';
      btn.classList.remove('playing');
      audio.pause();
      audio.currentTime = 0;
      msg.textContent = '';
    }
  }
  document.getElementById('chime-audio').addEventListener('ended', () => {
    const btn = document.querySelector('.bell-btn');
    btn.dataset.state = 'idle';
    btn.classList.remove('playing');
    document.querySelector('.bell-msg').textContent = '';
  });
</script>

I enjoy playing music. I play the [carillon](https://www.gcna.org/about-carillons) and am a Carillonneur member of the [Guild of Carillonneurs in North America (GCNA)](https://www.gcna.org/), having recently passed the [GCNA Carillonneur Exam](https://www.gcna.org/exam-carillonneur). I am fortunate to study the instrument with [Wesley Arai](https://music.ucsb.edu/people/faculty/wesley-arai) at UCSB, playing the [Storke Tower carillon](https://dailynexus.com/interactives/storke-tower-carillon/). You can find my progress videos and recordings [here](https://www.youtube.com/@roly4301). Previously, I studied organ with [Gail Archer](http://www.gailarcher.com/artist.html) at [Vassar](https://miscellanynews.org/2023/03/29/opinions/goodbye-vassar-organs-hello-panda-express/).
<!-- Even earlier, I studied piano as a child and (very superficially) dabbled in harp and violin. -->


<!-- <center>

<img src="/images/storke.jpg" alt="UCSB Storke Tower" title="Storke Tower" height="250" >
<img src="/images/chapel.jpg" alt="Vassar Chapel" title="Vassar Chapel (pc: Jacy Sun)" height="250" >

</center> -->

<center>
<button type="button" class="char-flip" aria-label="Flip character" onclick="flipChar(this)">あ</button>
</center>
<script>
  (function () {
    const chars = ['あ', 'A', '阿', '아'];
    window.flipChar = function (btn) {
      if (btn.classList.contains('flipping')) return;
      btn.classList.add('flipping');
      // Swap the visible character while the button is edge-on (mid-rotation).
      setTimeout(() => {
        const i = (parseInt(btn.dataset.idx || '0', 10) + 1) % chars.length;
        btn.textContent = chars[i];
        btn.dataset.idx = i;
      }, 300);
      setTimeout(() => btn.classList.remove('flipping'), 600);
    };
  })();
</script>

I also like learning languages. I studied Japanese in college and subsequently passed the JLPT N1 exam. I am mildly weeb, enjoying [owarai](https://www.youtube.com/@sissonnelive/videos), [podcasts](https://youtube.com/playlist?list=PLYpJvGKpl7tao5DG9RIaNpj9kyjv8irCV&si=j2ElqqSnmbupkc5Y), and [anime](/images/3x3.jpg).

<!-- <center>
<img src="/images/middlebury.jpg" alt="Middlebury" title="Middlebury" height="300">
</center> -->