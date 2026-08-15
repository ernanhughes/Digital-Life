(function () {
  'use strict';

  var button = document.querySelector('.menu__btn');
  var menu = document.querySelector('.menu__list');

  if (!button || !menu) {
    return;
  }

  button.addEventListener('click', function () {
    var expanded = button.getAttribute('aria-expanded') === 'true';
    button.setAttribute('aria-expanded', expanded ? 'false' : 'true');
    button.classList.toggle('menu__btn--active', !expanded);
    menu.classList.toggle('menu__list--active', !expanded);
  });
}());
