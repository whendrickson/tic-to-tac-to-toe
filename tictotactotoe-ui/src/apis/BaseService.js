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

import axios from 'axios';

axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';
axios.defaults.withCredentials = true;

export default class BaseService {
  static $http = axios;

  static urlGames = '/api/v1/games';

  static urlLogin = '/api/v1/login';

  static urlLogout = '/api/v1/logout';

  static urlRegister = '/api/v1/register';

  static urlWho = '/api/v1/who';

  static getRequest(URI, filters) {
    const params = new URLSearchParams();
    if (filters !== undefined) {
      Object.keys(filters).forEach((key) => {
        if (filters[key] !== undefined && filters[key] != null && filters[key] !== '') {
          params.append(key, filters[key]);
        }
      });
    }
    return this.$http.get(URI, { params })
      .then(this.extractPayload)
      .catch(this.errorHandler);
  }

  static postRequest(URI, DATA) {
    return this.$http.post(URI, DATA)
      .then(this.extractPayload)
      .catch(this.errorHandler);
  }

  static putRequest(URI, DATA) {
    return this.$http.put(URI, DATA)
      .then(this.extractPayload)
      .catch(this.errorHandler);
  }

  static deleteRequest(URI) {
    return this.$http.delete(URI, {})
      .then(this.extractPayload)
      .catch(this.errorHandler);
  }

  static extractPayload({ data, status }) {
    return {
      data,
      status,
    };
  }

  static errorHandler(error) {
    const httpStatusCodes = {
      400: 'Bad Request',
      401: 'Unauthorized',
      402: 'Payment Required',
      403: 'Forbidden',
      404: 'Not Found',
      405: 'Method Not Allowed',
    };
    let detailError = error.response.data.message;
    if (detailError === undefined) {
      detailError = httpStatusCodes[error.response.status];
    }
    return {
      data: error.response.data,
      message: detailError,
      status: error.response.status,
    };
  }
}
