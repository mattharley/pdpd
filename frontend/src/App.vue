<template>
  <div class="bg-gray-50 overflow-x-hidden">
    <Header />
    <Talks />
    <Photos />
    <Sponsors />
    <Code />
    <Conduct />
    <Footer />
  </div>
</template>

<script>
import Code from './components/Code.vue';
import Conduct from './components/Conduct.vue';
import Footer from './components/Footer.vue';
import Header from './components/Header.vue';
import Photos from './components/Photos.vue';
import Sponsors from './components/Sponsors.vue';
import Talks from './components/Talks.vue';

export default {
  components: {
    Code,
    Conduct,
    Footer,
    Header,
    Photos,
    Sponsors,
    Talks,
  }
};
</script>

