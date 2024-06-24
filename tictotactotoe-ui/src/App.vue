/**
 * Copyright 2024 Wes Hendrickson
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     https://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
*/

<script>
import ApiService from '@/apis/ApiService';
import TopHeaderBar from '@/components/TopHeaderBar.vue';
import ShowToast from '@/components/ShowToast.vue';
import { Toast } from 'bootstrap';
import { nextTick } from 'vue';
import { useRouter } from 'vue-router';

export default {
  setup() {
    const router = useRouter();
    return {
      router,
    };
  },
  data() {
    return {
      authenticated: false,
      toasts: [],
      user: undefined,
    };
  },
  name: 'App',
  components: {
    'show-toast': ShowToast,
    'top-header-bar': TopHeaderBar,
  },
  methods: {
    async pageChange(page, extra) {
      let i = 0;
      // for whatever reason page changes are not happening to force the router to change by looping
      while (i < 10) {
        if (this.router.currentRoute.value.name === page) {
          break;
        }
        /* eslint-disable no-await-in-loop */
        await this.router.push({ ...{ name: page }, ...extra });
        i += 1;
      }
    },
    async makeToast(variant, title, smallTitle, body) {
      const toastId = `toast${Date.now()}`;
      this.toasts.push({
        id: toastId,
        title,
        smallTitle,
        body,
        classHeader: `toast-header ${variant}`,
        classBody: 'toast-body',
      });
      await nextTick();
      const myToast = document.getElementById(toastId);
      new Toast(myToast).show();
      myToast.addEventListener('hidden.bs.toast', () => {
        this.toasts.shift();
      });
    },
    async who() {
      const me = await ApiService.who();
      if (me.status === 200) {
        if (this.authenticated) { return; }
        this.authenticated = true;
        this.user = me.data.data;
        if (this.$route.name === 'login') {
          this.pageChange('home');
        }
      } else {
        this.user = undefined;
        this.authenticated = false;
        if (this.$route.name !== 'login') {
          this.pageChange('login');
        }
      }
    },
  },
  async mounted() {},
};
</script>

<template>
  <div id="app">
    <div id="nav" style="position: fixed; width: 100%; z-index: 1;">
      <top-header-bar
        :pageChange="pageChange"
        :user="user"
      />
    </div>
    <RouterView
      :makeToast="makeToast"
      :pageChange="pageChange"
      :user="user"
      :who="who"
    />
    <div style="position: absolute; bottom: 0; right: 0; float: right;">
      <show-toast
        :toasts="toasts"
      />
    </div>
  </div>
</template>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
</style>
