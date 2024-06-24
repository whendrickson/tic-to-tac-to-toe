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
  <div class="top-header">
    <nav id="bg-custom" class="navbar navbar-expand-lg bg-body-tertiary">
      <div class="container-fluid">
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
          <ul class="navbar-nav me-auto mb-2 mb-lg-0">
            <li class="nav-item dropdown">
              <a
                class="navbar-brand dropdown-toggle"
                href="#"
                role="button"
                data-bs-toggle="dropdown"
                aria-expanded="false"
              >
                Tic-To-Tac-To-Toe
              </a>
              <ul class="dropdown-menu dropdown-menu-dark">
                <li><a class="dropdown-item" href="#" @click="pageChange('home')">Home</a></li>
                <li><a class="dropdown-item" href="#" @click="pageChange('about')">About</a></li>
                <li><hr class="dropdown-divider"></li>
                <li><a class="dropdown-item" href="#" @click="pageChange('logout')">Logout</a></li>
              </ul>
            </li>
          </ul>
          <div v-if="user">
            <p><strong>Hello {{ user.first_name }}!</strong></p>
          </div>
          <div v-else>
            <p><strong>Hello World!</strong></p>
          </div>
        </div>
      </div>
    </nav>
  </div>
</template>

<script>
export default {
  name: 'TopHeaderBar',
  props: ['pageChange', 'user'],
};
</script>

<style scoped>
#bg-custom {
  background-color: #383c44 !important;
}
p {
  color: #FFFFFF;
}
a {
  color: #FFFFFF;
  &:hover {
    color: #000000;
  }
}
</style>
