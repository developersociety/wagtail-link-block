/* global window */
(function() {
    'use strict';

    // Fields that should show the "new window" toggle when selected.
    const NEW_WINDOW_TYPES = ['page', 'custom_url', 'anchor'];

    function setRelatedFieldsVisibility(link_type_selector) {
        const value = link_type_selector.value;
        const parent = link_type_selector.closest('.link_block');

        // Hide all _link_field elements
        parent.querySelectorAll('[class*="_link_field"]').forEach(function(el) {
            el.classList.add('link-block__hidden');
        });

        if (value) {
            // Show the field matching the selected type
            const field = parent.querySelector('.' + value + '_link_field');
            if (field) {
                field.classList.remove('link-block__hidden');
            }

            // Show new_window toggle for applicable types
            const newWindowField = parent.querySelector('.new_window_link_field');
            if (newWindowField && NEW_WINDOW_TYPES.indexOf(value) !== -1) {
                newWindowField.classList.remove('link-block__hidden');
            }
        }
    }

    function onload() {
        const active_selectors = document.querySelectorAll('.link_choice_type_selector select');

        // Show link options if a link has been chosen
        // prototype call to make IE happy.
       Array.prototype.forEach.call(active_selectors, setRelatedFieldsVisibility);
    }

    function onchange(event) {
        const target = event.target,
            link_choice_div = target.closest('.link_choice_type_selector');

        if (link_choice_div !== null) {
            setRelatedFieldsVisibility(target);
        }
    }

    window.addEventListener('load', onload);
    window.addEventListener('change', onchange);

})();
