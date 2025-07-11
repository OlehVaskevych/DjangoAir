// eventBus.js

import mitt from 'mitt';

/**
 * Створюємо екземпляр mitt як Event Bus
 * mitt - це легка бібліотека для роботи з подіями (~200 байт)
 * Рекомендована для Vue 3 замість Vue instance event bus
 */
export const emitter = mitt();

/**
 * Константи подій для уникнення помилок при написанні назв подій
 * Використовуйте ці константи замість рядкових літералів
 */
export const EventTypes = {
  // Події авторизації
  AUTH: {
    OPEN_LOGIN_MODAL: 'auth:open-login-modal',
    OPEN_REGISTER_MODAL: 'auth:open-register-modal',
    CLOSE_AUTH_MODALS: 'auth:close-modals',
    LOGIN_SUCCESS: 'auth:login-success',
    LOGIN_ERROR: 'auth:login-error',
    REGISTER_SUCCESS: 'auth:register-success',
    REGISTER_ERROR: 'auth:register-error',
    LOGOUT: 'auth:logout'
  },
  
  // Події бронювання
  BOOKING: {
    PROCEED_TO_BOOKING: 'booking:proceed-to-booking',
    PROCEED_TO_SEATS: 'booking:proceed-to-seats',
    PROCEED_TO_PAYMENT: 'booking:proceed-to-payment',
    BOOKING_COMPLETE: 'booking:complete',
    BOOKING_ERROR: 'booking:error'
  },
  
  // Події навігації
  NAVIGATION: {
    CHANGE_SECTION: 'navigation:change-section',
    SCROLL_TO: 'navigation:scroll-to'
  },
  
  // Події сповіщень
  NOTIFICATION: {
    SHOW: 'notification:show',
    HIDE: 'notification:hide'
  }
};

/**
 * Допоміжні методи для роботи з Event Bus
 */
export const EventBusHelper = {
  /**
   * Відкриває модальне вікно входу
   * @param {Object} options - Додаткові параметри
   */
  openLoginModal(options = {}) {
    emitter.emit(EventTypes.AUTH.OPEN_LOGIN_MODAL, options);
  },

  /**
   * Відкриває модальне вікно реєстрації
   * @param {Object} options - Додаткові параметри
   */
  openRegisterModal(options = {}) {
    emitter.emit(EventTypes.AUTH.OPEN_REGISTER_MODAL, options);
  },

  /**
   * Закриває всі модальні вікна авторизації
   */
  closeAuthModals() {
    emitter.emit(EventTypes.AUTH.CLOSE_AUTH_MODALS);
  },

  /**
   * Сповіщає про успішний вхід
   * @param {Object} userData - Дані користувача
   */
  notifyLoginSuccess(userData) {
    emitter.emit(EventTypes.AUTH.LOGIN_SUCCESS, userData);
  },

  /**
   * Сповіщає про успішну реєстрацію
   * @param {Object} userData - Дані користувача
   */
  notifyRegisterSuccess(userData) {
    emitter.emit(EventTypes.AUTH.REGISTER_SUCCESS, userData);
  },

  /**
   * Змінює поточну секцію
   * @param {string} sectionName - Назва секції
   * @param {Object} options - Додаткові параметри
   */
  changeSection(sectionName, options = {}) {
    emitter.emit(EventTypes.NAVIGATION.CHANGE_SECTION, { section: sectionName, ...options });
  },

  /**
   * Показує сповіщення
   * @param {string} message - Текст сповіщення
   * @param {string} type - Тип сповіщення (success, error, warning, info)
   * @param {Object} options - Додаткові параметри
   */
  showNotification(message, type = 'info', options = {}) {
    emitter.emit(EventTypes.NOTIFICATION.SHOW, { message, type, ...options });
  }
};

/**
 * Приклад використання:
 *
 * Імпорт:
 * import { emitter, EventTypes } from './eventBus';
 *
 * Відправка події:
 * emitter.emit(EventTypes.AUTH.OPEN_LOGIN_MODAL, { redirectTo: 'booking' });
 *
 * Прослуховування події:
 * emitter.on(EventTypes.AUTH.OPEN_LOGIN_MODAL, (payload) => {
 *   // Обробка події
 *   console.log('Відкриваємо модальне вікно входу', payload);
 * });
 *
 * Прослуховування всіх подій:
 * emitter.on('*', (type, payload) => {
 *   console.log('Подія:', type, payload);
 * });
 *
 * Видалення прослуховувача:
 * const handler = (payload) => console.log(payload);
 * emitter.on(EventTypes.AUTH.OPEN_LOGIN_MODAL, handler);
 * // Пізніше, коли прослуховувач більше не потрібен:
 * emitter.off(EventTypes.AUTH.OPEN_LOGIN_MODAL, handler);
 *
 * Видалення всіх прослуховувачів для події:
 * emitter.off(EventTypes.AUTH.OPEN_LOGIN_MODAL);
 *
 * Видалення всіх прослуховувачів:
 * emitter.all.clear();
 */

export default emitter;