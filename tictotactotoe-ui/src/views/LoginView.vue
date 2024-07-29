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
  <div class="login">
    <top-header-spacer />
    <div>
      <h1>Welcome To Tic-To-Tac-To-Toe!!!</h1>
      <div class="container container-lg">
        <form autocomplete="off" @submit.prevent="login">
          <div class="row">
            <div class="col" />
            <div class="col">
              <!-- Username -->
              <div class="input-group mb-3">
                <span class="input-group-text" id="inputGroup-username">Username</span>
                <input
                  type="text"
                  class="form-control"
                  aria-label="input-username"
                  aria-describedby="inputGroup-username"
                  v-model="username"
                />
              </div>
              <!-- Username -->
              <div class="input-group mb-3">
                <span class="input-group-text" id="inputGroup-password">Password</span>
                <input
                  type="password"
                  class="form-control"
                  aria-label="input-password"
                  aria-describedby="inputGroup-password"
                  v-model="password"
                />
              </div>
              <button type="submit" class="btn btn-success me-1">Submit</button>
              <button type="button" class="btn btn-secondary me-1" @click="reset">Cancel</button>
              <button type="button" class="btn btn-warning me-1" @click="forgot">Forgot Password</button>
              <button type="button" class="btn btn-primary me-1" @click="register">Register!</button>
            </div>
            <div class="col" />
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import TopHeaderSpacer from '@/components/TopHeaderSpacer.vue';
import ApiService from '@/apis/ApiService';

export default {
  data() {
    return {
      username: undefined,
      password: undefined,
    };
  },
  methods: {
    forgot() {
      this.pageChange('forgot');
    },
    async login() {
      const apiResponse = await ApiService.loginUser(
        this.username,
        this.password,
      );
      if (apiResponse.status !== 202) {
        this.makeToast(
          'bg-danger',
          'Login',
          apiResponse.data.status.toUpperCase(),
          apiResponse.data.message,
        );
        return;
      }
      this.pageChange('home');
    },
    register() {
      this.pageChange('register');
    },
    reset() {
      this.username = undefined;
      this.password = undefined;
    },
  },
  async mounted() {
    await this.who();
  },
  created() {},
  name: 'LoginView',
  components: {
    'top-header-spacer': TopHeaderSpacer,
  },
  props: ['makeToast', 'pageChange', 'who'],
};
</script>
