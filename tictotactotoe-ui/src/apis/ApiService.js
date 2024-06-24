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

import BaseService from './BaseService';

export default class JsonApiService extends BaseService {
  static createGames(name) {
    return this.postRequest(this.urlGames, {
      name,
    });
  }

  static requestGames() {
    return this.getRequest(this.urlGames, {});
  }

  static updateGame(gameId, player) {
    return this.putRequest(`${this.urlGames}/${gameId}`, {
      player,
    });
  }

  static createMove(gameId, x, y) {
    return this.postRequest(`${this.urlGames}/${gameId}/moves`, {
      x,
      y,
    });
  }

  static loginUser(username, password) {
    return this.postRequest(this.urlLogin, {
      username,
      password,
    });
  }

  static logoutUser() {
    return this.postRequest(this.urlLogout, {});
  }

  static registerUser(username, password, password2, email, firstName, lastName) {
    return this.postRequest(this.urlRegister, {
      username,
      password,
      password2,
      email,
      first_name: firstName,
      last_name: lastName,
    });
  }

  static requestGame(gameId) {
    return this.getRequest(`${this.urlGames}/${gameId}`, {});
  }

  static who() {
    return this.getRequest(this.urlWho, {});
  }
}
