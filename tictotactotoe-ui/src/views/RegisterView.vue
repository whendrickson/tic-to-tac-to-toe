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
  <div class="register">
    <top-header-spacer />
    <div>
      <h1>Please fill out this form to Register for Tic-To-Tac-To-Toe!!!</h1>
      <div class="container container-lg">
        <form autocomplete="off" @submit.prevent="register">
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
                  pattern="^[a-zA-Z\d\.]{6,30}$"
                  oninvalid="this.setCustomValidity('Sorry, only letters (a-z), numbers (0-9), and periods (.) are allowed. Must be between 6 and 30 characters long.')"
                  onchange="try{setCustomValidity('')}catch(e){}"
                  oninput="setCustomValidity(' ')"
                  required
                />
              </div>
              <!-- Password -->
              <div class="input-group mb-3">
                <span class="input-group-text" id="inputGroup-password">Password</span>
                <input
                  id="password"
                  type="password"
                  class="form-control"
                  aria-label="input-password"
                  aria-describedby="inputGroup-password"
                  v-model="password"
                  required
                  :onChange="verifyPass()"
                />
              </div>
              <!-- Password2 -->
              <div class="input-group mb-3">
                <span class="input-group-text" id="inputGroup-password2">Confirm</span>
                <input
                  id="password2"
                  type="password"
                  class="form-control"
                  aria-label="input-password2"
                  aria-describedby="inputGroup-password2"
                  v-model="password2"
                  required
                  :onChange="verifyPass()"
                />
              </div>
              <!-- Email -->
              <div class="input-group mb-3">
                <span class="input-group-text" id="inputGroup-email">Email</span>
                <input
                  type="email"
                  class="form-control"
                  aria-label="input-email"
                  aria-describedby="inputGroup-email"
                  v-model="email"
                  required
                />
              </div>
              <!-- First Name -->
              <div class="input-group mb-3">
                <span class="input-group-text" id="inputGroup-first">First Name</span>
                <input
                  type="text"
                  class="form-control"
                  aria-label="input-first"
                  aria-describedby="inputGroup-first"
                  v-model="firstName"
                  required
                />
              </div>
              <!-- Last Name -->
              <div class="input-group mb-3">
                <span class="input-group-text" id="inputGroup-last">Last Name</span>
                <input
                  type="text"
                  class="form-control"
                  aria-label="input-last"
                  aria-describedby="inputGroup-last"
                  v-model="lastName"
                  required
                />
              </div>
              <button type="submit" class="btn btn-success me-1">Register</button>
              <button type="button" class="btn btn-secondary me-1" @click="reset">Cancel</button>
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
      password2: undefined,
      email: undefined,
      firstName: undefined,
      lastName: undefined,
    };
  },
  methods: {
    async register() {
      const apiResponse = await ApiService.registerUser(
        this.username,
        this.password,
        this.password2,
        this.email,
        this.firstName,
        this.lastName,
      );
      if (apiResponse.status !== 201) {
        this.makeToast(
          'bg-danger',
          'Register',
          'ERROR',
          apiResponse.data
        );
        return;
      }
      this.pageChange('login');
    },
    reset() {
      this.username = undefined;
      this.password = undefined;
      this.password2 = undefined;
      this.email = undefined;
      this.firstName = undefined;
      this.last_name = undefined;
    },
    verifyPass() {
      const docPassword = document.getElementById('password');
      const docPassword2 = document.getElementById('password2');
      if (docPassword === null || this.password === undefined) { return; }
      if (docPassword2 === null || this.password2 === undefined) { return; }
      if (this.password === this.password2) {
        docPassword.classList.remove('is-invalid');
        docPassword.classList.add('is-valid');
        docPassword2.classList.remove('is-invalid');
        docPassword2.classList.add('is-valid');
      } else {
        docPassword.classList.remove('is-valid');
        docPassword.classList.add('is-invalid');
        docPassword2.classList.remove('is-valid');
        docPassword2.classList.add('is-invalid');
      }
    },
  },
  mounted() {},
  created() {},
  name: 'RegisterView',
  components: {
    'top-header-spacer': TopHeaderSpacer,
  },
  props: ['makeToast', 'pageChange'],
};
</script>
