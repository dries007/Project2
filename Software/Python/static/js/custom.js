"use strict";
/** on load */
const TAB_STATUS = $('a[data-toggle="tab"][href="#status"]');
const TAB_WIFI = $('a[data-toggle="tab"][href="#wifi"]');
const TAB_CLOCK = $('a[data-toggle="tab"][href="#clock"]');
const TAB_GCAL = $('a[data-toggle="tab"][href="#gcal"]');

const MODAL = $('#modal');
const DEBUG = $('#debug');

const GCAL_STATUS = $('#gcal-status');

var status_data = null;
var wifi_data = null;

function disableTabs() {
    [TAB_STATUS, TAB_WIFI, TAB_CLOCK, TAB_GCAL].forEach(function (e)
    {
        e.prop('disabled', true).addClass('disabled')
    });
}

function enableTabs() {
    [TAB_STATUS, TAB_WIFI, TAB_CLOCK, TAB_GCAL].forEach(function (e)
    {
        e.prop('disabled', false).removeClass('disabled')
    });
}

function showModal(message, title)
{
    disableTabs();
    MODAL.find('.modal-body').text(message);
    MODAL.find('.modal-title').text(title);
    MODAL.modal({backdrop: 'static', keyboard: false, show: true});
}

function loadStatus()
{
    disableTabs();
    $.getJSON('/api/status', function (data)
    {
        console.log('Update status data.');
        status_data = data;
        DEBUG.text(JSON.stringify(data, null, 4));
        if (data['booting']) return;
        MODAL.modal('hide');
        enableTabs();
        clearTimeout(showTimeout);
        if (!data['network']) TAB_WIFI.tab('show');
        else if (data['gcal']['user_code']) TAB_GCAL.tab('show');
    }).error(function ()
    {
        setTimeout(loadStatus, 500);
    });
}

if (document.location.toString().match('#'))
{
    $('.nav-tabs a[href="#' + document.location.toString().split('#')[1] + '"]').tab('show');
}
$('.nav-tabs a').on('shown.bs.tab', function (e)
{
    loadStatus();
    window.location.hash = e.target.hash;
});

var showTimeout = setTimeout(function()
{
    showModal('The program is still booting...', 'Please wait');
}, 250);
loadStatus();

// WiFi tab
const WIFI_DROPDOWN = $('#wifi-dropdown');
const WIFI_FORM = $('#wifi-form');
const WIFI_RELOAD = $('#wifi-reload');
const WIFI_SSID = $('#wifi-ssid');
const WIFI_PASS = $('#wifi-pass');

function onChangeSSID()
{
    WIFI_SSID.parents('.form-group').removeClass('has-error');
    WIFI_DROPDOWN.parents('.form-group').removeClass('has-error');
    // index of selected option, or -1
    var i = WIFI_DROPDOWN.val();
    if (i != -1) // One of the items on the list
    {
        WIFI_PASS.val('').attr('readonly', wifi_data[i].Protected == 'off');
        WIFI_SSID.val(wifi_data[i].SSID).attr('readonly', true);
    }
    else // Manual
    {
        WIFI_SSID.attr('readonly', false).val('');
        WIFI_PASS.attr('readonly', false).val('');
    }
}

function loadWifi()
{
    WIFI_RELOAD.prop('disabled', true);
    disableTabs();
    WIFI_DROPDOWN.html('<option value="-1" disabled>Scanning...</option>');
    $.getJSON('/api/wifi', function (data)
    {
        wifi_data = data;
        var html = "<option value='-1' disabled selected>Pick an option...</option>";
        for (var i = 0; i < data.length; i++)
        {
            if (data[i].SSID === "") continue;
            html += "<option value='" + i + "'" + (data[i].Authentication === '802.1x' ? ' disabled ' : '') + ">" + data[i].SSID + "</option>";
        }
        html += "<option value='-1'>Other...</option>";
        WIFI_DROPDOWN.html(html);
        WIFI_RELOAD.prop('disabled', false);
        enableTabs();
    });
}
WIFI_RELOAD.click(function () {
    loadWifi();
});
WIFI_DROPDOWN.change(onChangeSSID);
WIFI_SSID.focusin(function ()
{
    WIFI_SSID.parents('.form-group').removeClass('has-error');
});
WIFI_FORM.submit(function ()
{
    if (WIFI_SSID.val() == '')
    {
        if (WIFI_DROPDOWN.val() == -1) WIFI_SSID.parents('.form-group').addClass('has-error');
        else WIFI_DROPDOWN.parents('.form-group').addClass('has-error');
        return false;
    }

    disableTabs();
    showModal('Connecting to the wifi network...<br>Make sure you connect to the same wifi as the SmartAlarmClock.', 'Connecting to wifi');
    $.post('/api/wifi', {ssid: WIFI_SSID.val(), pass: WIFI_PASS.val()}, function ()
    {
        MODAL.modal('hide');
        enableTabs();
    });

    return false;
});


// Clock tab
function setBnt(jq, b)
{
    if (b) jq.removeClass('btn-danger').addClass('btn-success').text('Enabled');
    else jq.removeClass('btn-success').addClass('btn-danger').text('Disabled');
}

function toggleBnt()
{
    var us = $(this);
    setBnt(us, !us.hasClass('btn-success'));
}

const CLOCK_FORM = $("#clock-form");
const CLOCK_WEEKDAY_ENABLE = $("#clock-weekday-enable").click(toggleBnt);
const CLOCK_WEEKDAY_SIZE = $("#clock-weekday-size");
const CLOCK_FORMAT1 = $("#clock-format1");
const CLOCK_SIZE1 = $("#clock-size1");
const CLOCK_FORMAT2_ENABLE = $("#clock-format2-enable").click(toggleBnt);;
const CLOCK_FORMAT2 = $("#clock-format2");
const CLOCK_SIZE2 = $("#clock-size2");
const CLOCK_OFFSET = $("#clock-offset");
const CLOCK_MIN = $("#clock-min");
const CLOCK_MIN_ENABLE = $("#clock-min-enable").click(toggleBnt);
const CLOCK_MAX = $("#clock-max");
const CLOCK_MAX_ENABLE = $("#clock-max-enable").click(toggleBnt);
const CLOCK_DAYS_1 = $("#clock-days-1");
const CLOCK_DAYS_2 = $("#clock-days-2");
const CLOCK_DAYS_3 = $("#clock-days-3");

//const ALARMTYPE = $("#alarmtype");

//Global things
TAB_STATUS.on('show.bs.tab', function ()
{
    console.log('Tab status');
});
TAB_WIFI.on('show.bs.tab', function ()
{
    console.log('Tab wifi');
    loadWifi();
});
TAB_CLOCK.on('show.bs.tab', function ()
{
    console.log('Tab clock');
});
TAB_GCAL.on('show.bs.tab', function ()
{
    console.log('Tab gcal');
});