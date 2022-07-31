/* ------------------------------------------------------------------------------
 *
 *  # Sweet Alert component
 *
 *  Demo JS code for extra_sweetalert.html page
 *
 * ---------------------------------------------------------------------------- */


// Setup module
// ------------------------------

var SweetAlert = function () {


    //
    // Setup module components
    //

    // Sweet Alerts
    var _componentSweetAlert = function() {
        if (typeof swal == 'undefined') {
            console.warn('Warning - sweet_alert.min.js is not loaded.');
            return;
        }

        // Defaults
        var swalInit = swal.mixin({
            buttonsStyling: false,
            customClass: {
                confirmButton: 'btn btn-primary',
                cancelButton: 'btn btn-light',
                denyButton: 'btn btn-light',
                input: 'form-control'
            }
        });
    };

    return {
        initComponents: function() {
            _componentSweetAlert();
        }
    }
}();

// Initialize module
// ------------------------------

document.addEventListener('DOMContentLoaded', function() {
    SweetAlert.initComponents();
});