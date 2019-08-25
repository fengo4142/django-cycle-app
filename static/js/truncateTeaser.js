(function ($) {
    /**
     * Shorten a text until it's below a certain heigt.
     * Pass the parameter 'height' in px with the options.
     * 
     * Usage:
     * 
     * $('.teasers').truncateTeasers({height: 40});
     * 
     * This removes words from the end of the text in all .teasers
     * until it is lower than 40px.
     * 
     * WARNING: This script will be inefficient if you have very long
     * captions everywhere.
     * 
     **/

    'use strict';

    var element_too_high = function ($element, max_height) {
            return $element.height() > max_height;
        },
        stripDots = function (text) {
            var splitIndex = text.length - 4,
                lastCharacters = text.substr(splitIndex);
            if (lastCharacters === ' ...') {
                text = text.substr(0, splitIndex);
            }
            return text;
        },
        removeLastWord = function ($element) {
            var text = stripDots($element.text()),
                lastIndex = text.lastIndexOf(" "),
                shorter_text = text.substring(0, lastIndex);
            $element.text(shorter_text + ' ...');
        };

    jQuery.fn.truncateTeasers = function (options) {
        return this.each(function () {
            while (element_too_high($(this), options.height)) {
                removeLastWord($(this));
            }
        });
    };
}(jQuery));