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

<template>
  <div class="logout">
    <top-header-spacer />
    <div>
      <h1>This is the about page!</h1>
      <div>
        I should write something more this works for now!
      </div>
    </div>
  </div>
</template>

<script>
import TopHeaderSpacer from '@/components/TopHeaderSpacer.vue';
import ApiService from '@/apis/ApiService';

export default {
  data() {
    return {};
  },
  methods: {
    async logout() {
      const apiResponse = await ApiService.logoutUser();
      if (apiResponse.status !== 202) {
        this.makeToast(
          'bg-danger',
          'Logout',
          'ERROR',
          'Something went wrong!',
        );
        return;
      }
      this.pageChange('login');
    },
  },
  mounted() {
    this.logout();
  },
  name: 'LogoutView',
  components: {
    'top-header-spacer': TopHeaderSpacer,
  },
  props: ['makeToast', 'pageChange'],
};
</script>
