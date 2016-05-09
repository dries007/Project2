"use strict";

/** on load */
$(function ()
{
    const MODAL = $("#modal");
    const DEBUG = $("#debug");
    const TAB_WIFI = $("#wifi");

    function loadStatus()
    {
        function showModal()
        {
            MODAL.modal({backdrop: "static", keyboard: false, show: true});
        }
        var showTimeout = setTimeout(showModal, 250);
        $.getJSON("/api/status", function (data)
        {
            DEBUG.text(JSON.stringify(data, null, 4));
            MODAL.modal('hide');
            clearTimeout(showTimeout);
            if (!data.network) TAB_WIFI.tab('show');
        }).error(function ()
        {
            setTimeout(loadStatus, 500);
        });
    }

    loadStatus();
});
