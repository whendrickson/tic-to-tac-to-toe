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
  <div class="show-toast">
    <div
      id="myToastContainer"
      class="toast-container position-static"
      v-for="toast in toasts"
      :key="toast.id"
    >
      <div
        class="toast"
        role="alert"
        aria-live="assertive"
        aria-atomic="true"
        :id="toast.id"
        :ref="toast.id"
      >
        <div :class="toast.classHeader">
          <strong class="me-auto">{{ toast.title }}</strong>
          <small class="text-muted">{{ toast.smallTitle }}</small>
          <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close" />
        </div>
        <div :class="toast.classBody">
          {{ toast.body }}
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ShowToast',
  props: ['toasts'],
};
</script>
