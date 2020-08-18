/* global window */
(function() {
    'use strict';

    // For Links, only show the selected field types.  So if 'Page Link' is selected,
    // only show the Page Chooser.  If URL field, only show the URL field. Etc.

    function setRelatedFieldsVisibility(link_type_selector) {
        const value = link_type_selector.value;
        const parent = link_type_selector.closest('.link_block'),
            page_link = parent.querySelector('.page_link_field'),
            file_link = parent.querySelector('.file_link_field'),
            custom_url_link = parent.querySelector('.custom_url_link_field'),
            new_window_toggle = parent.querySelector('.new_window_link_field');

        // this is repetative, but I don't mind.  No magic.
        if (value === 'page') {
            page_link.classList.remove('link-block__hidden');
            file_link.classList.add('link-block__hidden');
            custom_url_link.classList.add('link-block__hidden');
            new_window_toggle.classList.remove('link-block__hidden');
        } else if (value === 'file') {
            page_link.classList.add('link-block__hidden');
            file_link.classList.remove('link-block__hidden');
            custom_url_link.classList.add('link-block__hidden');
            new_window_toggle.classList.add('link-block__hidden');
        } else if (value === 'custom_url') {
            page_link.classList.add('link-block__hidden');
            file_link.classList.add('link-block__hidden');
            custom_url_link.classList.remove('link-block__hidden');
            new_window_toggle.classList.remove('link-block__hidden');
        } else {
            page_link.classList.add('link-block__hidden');
            file_link.classList.add('link-block__hidden');
            custom_url_link.classList.add('link-block__hidden');
            new_window_toggle.classList.add('link-block__hidden');
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
