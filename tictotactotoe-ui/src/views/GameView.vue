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
  <div class="game" align="center">
    <top-header-spacer />
    <div>
      <div>
        <table style="width: 100%;">
          <tbody>
            <tr>
              <td style="vertical-align: top;width: 10%;">
                <div>
                  <b>Game: {{ name }}!</b>
                </div>
                <div v-if="symbol">
                  <b>Symbol: {{ symbol }}</b>
                </div>
                <div>
                  <b>{{ prettyState(state) }}</b>
                </div>
                <span v-if="!playerX">
                  <button type="button" class="btn btn-success me-1" @click="play('x')">Play X</button>
                </span>
                <span v-if="!playerO">
                  <button type="button" class="btn btn-success me-1" @click="play('o')">Play O</button>
                </span>
              </td>
              <td style="width: 90%;">
                <table class="table">
                  <tbody>
                    <tr v-for="(rows, y_idx) in moves" style="height: 34%;">
                      <td
                        style="vertical-align: middle; width: 30%;"
                        v-for="(move, x_idx) in rows"
                        @click="clickMade(x_idx, y_idx)"
                      >
                        <div style="font-size:120px;">
                          <b>{{ move }}</b>
                        </div>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import { useRoute } from 'vue-router';
import ApiService from '@/apis/ApiService';
import MessageBoxConfirm from '@/components/MessageBoxConfirm.vue';
import PrettyStates from '@/components/PrettyStates.vue'
import TopHeaderSpacer from '@/components/TopHeaderSpacer.vue';

export default {
  data() {
    return {
      playerX: undefined,
      playerO: undefined,
      gameId: undefined,
      moves: [
        ['x', 'o', 'x'],
        ['o', 'o', 'x'],
        ['x', 'x', 'o'],
      ],
      name: 'XYZ',
      state: 'Tie Game!',
      symbol: undefined,
      tableColspan: 3,
      timer: '',
    };
  },
  methods: {
    clearTimer() {
      clearInterval(this.timer);
    },
    async clickMade(x, y) {
      const confirm = await MessageBoxConfirm.confirm(
        'Making a Move on the Board!',
        `Are you sure you want to move at x: ${x}, y: ${y}?`,
      );
      if (!confirm) { return; }
      let variant = 'bg-danger';
      const apiResponse = await ApiService.createMove(this.gameId, x, y);
      if (apiResponse.status === 201) {
        variant = 'bg-success';
      }
      this.makeToast(
        variant,
        'Move',
        apiResponse.data.status.toUpperCase(),
        apiResponse.data.message,
      );
      this.gameGet();
    },
    async gameGet() {
      const game = await ApiService.requestGame(this.gameId);
      if (game.status !== 200) {
        this.makeToast(
          'bg-danger',
          'Games',
          game.data.status.toUpperCase(),
          game.data.message,
        );
        return;
      }
      this.moves = game.data.data.moves;
      this.name = game.data.data.name;
      this.state = game.data.data.state;
      this.symbol = undefined;
      if (game.data.data.player_o !== null) {
        this.playerO = game.data.data.player_o;
        if (this.playerO.username === this.user.username) {
          this.symbol = 'O';
        }
      }
      if (game.data.data.player_x !== null) {
        this.playerX = game.data.data.player_x;
        if (this.playerX.username === this.user.username) {
          this.symbol = 'X';
        }
      }
    },
    async play(player) {
      const apiResponse = await ApiService.updateGame(this.gameId, player);
      let variant = 'bg-danger';
      if (apiResponse.status === 202) {
        variant = 'bg-success';
      }
      this.makeToast(
        variant,
        'Play',
        apiResponse.data.status.toUpperCase(),
        apiResponse.data.message,
      );
      this.gameGet();
    },
    prettyState(state) {
      return PrettyStates.pretty(state);
    },
  },
  async mounted() {
    const { gameId } = useRoute().params;
    await this.who();
    this.gameId = gameId;
    this.gameGet();
    this.timer = setInterval(this.gameGet, 30000); // Fetch data from API every minute
  },
  beforeUnmount() {
    this.clearTimer();
  },
  name: 'GameView',
  components: {
    'top-header-spacer': TopHeaderSpacer,
  },
  props: ['makeToast', 'user', 'who'],
};
</script>

<style scoped>
table {
    border-collapse: collapse;
    border-style: hidden;
    height:92vh;
}
table td {
    border: 1px solid black;
}
td {
    text-align:center;
    white-space:nowrap;
}
table td:hover {
    background-color: rgba(0,0,0,.075);
}
</style>