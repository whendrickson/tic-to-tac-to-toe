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
  <div class="home">
    <top-header-spacer />
    <div>
      <table class="table table-hover table-sm caption-top table-responsive" style="width:100%">
        <thead class="table-dark">
          <tr>
            <th style="text-align:left;width:1%;">
              <button
                type="button"
                class="btn btn-success btn-sm"
                @click="showGamesModal()"
                data-bs-toggle="tooltip"
                title="Create New Game!"
              >
                <i class="bi bi-file-plus-fill" />
              </button>
            </th>
            <th>Name</th>
            <th>State</th>
            <th>Player O</th>
            <th>Player X</th>
          </tr>
        </thead>
        <tbody v-for="g in games" :key="g.id">
          <tr @click="pageChange('game', { params: {gameId: g.id} })">
            <td></td>
            <td>{{ g.name }}</td>
            <td>{{ prettyState(g.state) }}</td>
            <td>
              <span v-if="g.player_o">{{ g.player_o.username }}</span>
            </td>
            <td>
              <span v-if="g.player_x">{{ g.player_x.username }}</span>
            </td>
          </tr>
        </tbody>
        <tfoot>
          <tr class="table-secondary">
            <td colspan="5" style="text-align:right;">
              <span v-if="games">Total Rows: <strong>{{ games.length }}</strong></span>
              <span v-else>Total Rows: <strong>0</strong></span>
            </td>
          </tr>
        </tfoot>
      </table>
    </div>
    <!-- Modal -->
    <div
      class="modal"
      id="gamesModal"
      tabIndex="-1"
      aria-labelledby="gamesModalLabel"
      aria-hidden="true"
      ref="gamesModal"
    >
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5" id="gamesModalLabel">Create a new game!</h1>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close" />
          </div>
          <div class="modal-body">
            <div class="input-group mb-3">
              <span class="input-group-text" id="inputGroup-name">Name</span>
              <input
                type="text"
                class="form-control"
                aria-label="input-name"
                aria-describedby="inputGroup-name"
                v-model="gamesModal.values.name"
              />
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
            <button
              type="button"
              class="btn btn-success"
              @click="saveGamesModal"
            >
              Save
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { Modal } from 'bootstrap';
import ApiService from '@/apis/ApiService';
import PrettyStates from '@/components/PrettyStates.vue'
import TopHeaderSpacer from '@/components/TopHeaderSpacer.vue';

export default {
  data() {
    return {
      games: [],
      gamesModal: {
        values: {
          name: undefined,
        },
      },
    };
  },
  methods: {
    async gamesGet() {
      const apiResponse = await ApiService.requestGames();
      if (apiResponse.status !== 200) {
        this.makeToast(
          'bg-danger',
          'Games',
          apiResponse.data.status.toUpperCase(),
          apiResponse.data.message,
        );
        return;
      }
      this.games = apiResponse.data.data;
    },
    prettyState(state) {
      return PrettyStates.pretty(state);
    },
    async saveGamesModal() {
      const apiResponse = await ApiService.createGames(this.gamesModal.values.name);
      if (apiResponse.status !== 201) {
        this.makeToast(
          'bg-danger',
          'Games',
          apiResponse.data.status.toUpperCase(),
          apiResponse.data.message,
        );
        return;
      }
      Modal.getInstance(document.getElementById('gamesModal')).hide();
      this.pageChange('game', { params: {gameId: apiResponse.data.data.id} });
    },
    showGamesModal() {
      new Modal(this.$refs.gamesModal).show();
    },
  },
  async mounted() {
    await this.who();
    this.gamesGet();
  },
  created() {},
  name: 'HomeView',
  components: {
    'top-header-spacer': TopHeaderSpacer,
  },
  props: ['makeToast', 'pageChange', 'who'],
};
</script>
