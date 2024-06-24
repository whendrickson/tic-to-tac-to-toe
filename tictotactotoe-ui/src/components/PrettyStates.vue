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
// todo: there is probably a more proper way to export this but this works for now
export default {
  pretty(state) {
    const states = {
      tie: 'Game ended in Tie!',
      turn_o: 'O\'s Turn',
      turn_x: 'X\'s Turn',
      winner_o: 'O is the WINNER!',
      winner_x: 'X is the WINNER!',
    };
    return states[state];
  },
  methods: {},
  name: 'PrettyStates',
};
</script>
