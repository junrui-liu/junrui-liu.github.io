+++
title = "Misc"
menu = "main"
weight = 30
+++

<center>
<button class="bell-btn" type="button" aria-label="Play or stop chime" onclick="toggleChime(this)">🔔</button>
<audio id="chime-audio" src="/audio/waltz.mp3" preload="metadata"></audio>
</center>
<script>
  function toggleChime(btn) {
    const a = document.getElementById('chime-audio');
    if (a.paused) {
      a.currentTime = 0;
      a.play();
      btn.classList.add('playing');
    } else {
      a.pause();
      a.currentTime = 0;
      btn.classList.remove('playing');
    }
  }
  document.getElementById('chime-audio').addEventListener('ended', () => {
    document.querySelector('.bell-btn').classList.remove('playing');
  });
</script>

I enjoy playing music, and am currently studying the [carillon](https://dailynexus.com/interactives/storke-tower-carillon/) with [Wesley Arai](https://music.ucsb.edu/people/faculty/wesley-arai). You can find my progress videos [here](https://www.youtube.com/@roly4301). Previously, I studied organ with [Gail Archer](http://www.gailarcher.com/artist.html) at [Vassar](https://miscellanynews.org/2023/03/29/opinions/goodbye-vassar-organs-hello-panda-express/). 


<!-- <center>

<img src="/images/storke.jpg" alt="UCSB Storke Tower" title="Storke Tower" height="250" >
<img src="/images/chapel.jpg" alt="Vassar Chapel" title="Vassar Chapel (pc: Jacy Sun)" height="250" >

</center> -->

<center>
あ
</center>

I also like learning languages. I studied Japanese in college and subsequently passed the JLPT N1 exam. I am mildly weeb, enjoying [owarai](https://www.youtube.com/@sissonnelive/videos), [podcasts](https://youtube.com/playlist?list=PLYpJvGKpl7tao5DG9RIaNpj9kyjv8irCV&si=j2ElqqSnmbupkc5Y), and [anime](/images/3x3.jpg). Currently learning Korean!

<!-- <center>
<img src="/images/middlebury.jpg" alt="Middlebury" title="Middlebury" height="300">
</center> -->