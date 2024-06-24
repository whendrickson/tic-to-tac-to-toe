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
import { Modal } from 'bootstrap';

export default {
  async confirm(title, body) {
    return this.methods.bConfirm(title, body);
  },
  methods: {
    async bConfirm(title, body) {
      const modalElem = document.createElement('div');
      modalElem.id = 'modal-confirm';
      modalElem.className = 'modal';
      modalElem.innerHTML = `
    <div class="modal-dialog modal-dialog-scrollable">
      <div class="modal-content">
        <div class="modal-header">
            <h5 class="modal-title">${title}</h5>
        </div>
        <div class="modal-body">
          <p>${body}</p>
        </div>
        <div class="modal-footer" style="border-top:0">
            <button id="modal-btn-confirm-cancel" type="button" class="btn btn-secondary">Cancel</button>
            <button id="modal-btn-confirm-accept" type="button" class="btn btn-primary">Accept</button>
        </div>
      </div>
    </div>
  `;
      const myModal = new Modal(modalElem, {
        keyboard: false,
      });
      myModal.show();

      return new Promise((resolve) => {
        function response(e) {
          let bool = false;
          if (e.target.id === 'modal-btn-confirm-cancel') bool = false;
          else if (e.target.id === 'modal-btn-confirm-accept') bool = true;
          else return;
          document.body.removeEventListener('click', response);
          myModal.hide();
          myModal.dispose();
          // document.body.querySelector('.modal-backdrop').remove();
          modalElem.remove();
          resolve(bool);
        }
        document.body.addEventListener('click', response);
      });
    },
  },
  name: 'MessageBoxConfirm',
};
</script>
