"use strict";
/** on load */
const TAB_STATUS = $('a[data-toggle="tab"][href="#status"]');
const TAB_WIFI = $('a[data-toggle="tab"][href="#wifi"]');
const TAB_CLOCK = $('a[data-toggle="tab"][href="#clock"]');
const TAB_GCAL = $('a[data-toggle="tab"][href="#gcal"]');

const MODAL = $('#modal');
const DEBUG = $('#debug');

const GCAL_RESET = $('#gcal-reset');
const GCAL_LINK = $('#gcal-link');
const GCAL_LIST = $('#gcal-list');
const GCAL_LIST_FORM = $('#gcal-list-form'); // todo: make useful
const GCAL_RESET_FORM = $('#gcal-reset-form');
const GCAL_LIST_ITEMS = $('#gcal-list-items');

var settings_timeout = null;

var status_data = null;
var settings_data = null;
var wifi_data = null;

function pad(n, width, z)
{
    z = z || '0';
    n = n + '';
    return n.length >= width ? n : new Array(width - n.length + 1).join(z) + n;
}

function minToTime(min)
{
    return pad(min / 60, 2) + ':' + pad(min % 60, 2);
}

function timeToMin(time)
{
    var split = time.split(':');
    return (parseInt(split[0]) * 60) + parseInt(split[1]);
}

function disableTabs()
{
    [TAB_STATUS, TAB_WIFI, TAB_CLOCK, TAB_GCAL].forEach(function (e)
    {
        e.prop('disabled', true).addClass('disabled')
    });
}

function enableTabs()
{
    [TAB_STATUS, TAB_WIFI, TAB_CLOCK, TAB_GCAL].forEach(function (e)
    {
        e.prop('disabled', false).removeClass('disabled')
    });
}

function showModal(message, title)
{
    disableTabs();
    MODAL.find('.modal-body').html(message);
    MODAL.find('.modal-title').html(title);
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
        loadSettings();
        clearTimeout(showTimeout);
        if (!data['network']) TAB_WIFI.tab('show');
        else if (data['gcal']['user_code'])
        {
            GCAL_LINK.show();
            GCAL_LIST.hide();
            GCAL_RESET.hide();
            $('#gcal-link-url').text(data['gcal']['verification_url']).attr('href', data['gcal']['verification_url']);
            $('#gcal-link-code').text(data['gcal']['user_code']);
            TAB_GCAL.tab('show');
            setTimeout(loadStatus, 2000);
        }
        else if (data['gcal']['access_token'])
        {
            GCAL_LIST.show();
            GCAL_LINK.hide();
            GCAL_RESET.show();
        }
        else if (data['gcal'])
        {
            GCAL_RESET.show();
        }

        if (data['items'])
        {
            GCAL_LIST_ITEMS.empty();
            data['items'].forEach(function (item)
            {
                GCAL_LIST_ITEMS.append('<li><b>' + item['summary'] + '</b> at ' + item['start']['dateTime'] + '</li>')
            })
        }

    }).error(function ()
    {
        setTimeout(loadStatus, 500);
    });
}

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
        loadStatus();
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
const CLOCK_FORMAT2_ENABLE = $("#clock-format2-enable").click(toggleBnt);
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

CLOCK_FORM.submit(function ()
{
    $.ajax({
        type: 'POST',
        url: '/api/settings',
        data: JSON.stringify(
            {
                'day': {
                    'enabled': CLOCK_WEEKDAY_ENABLE.hasClass('btn-success'),
                    'size': parseInt(CLOCK_WEEKDAY_SIZE.val())
                },
                'clock': {
                    'format': CLOCK_FORMAT1.val(),
                    'size': parseInt(CLOCK_SIZE1.val())
                },
                'date': {
                    'enabled': CLOCK_FORMAT2_ENABLE.hasClass('btn-success'),
                    'format': CLOCK_FORMAT2.val(),
                    'size': parseInt(CLOCK_SIZE2.val())
                },
                'alarm': {
                    'offset': CLOCK_OFFSET.val(),
                    'min': CLOCK_MIN_ENABLE.hasClass('btn-success') ? timeToMin(CLOCK_MIN.val()) : -1,
                    'max': CLOCK_MAX_ENABLE.hasClass('btn-success') ? timeToMin(CLOCK_MAX.val()) : -1,
                    'days': $('input:radio[name="clock-days"]:checked').val()
                }
            }),
        contentType: 'application/json',
        dataType: 'json',
        success: function ()
        {
            loadStatus();
            loadSettings();
        }
    });
    return false;
});

//Settings tabs
function loadSettings()
{
    $.getJSON('/api/settings', function (data)
    {
        console.log('Update settings data.');
        settings_data = data;
        setBnt(CLOCK_WEEKDAY_ENABLE, data['day']['enabled']);
        CLOCK_WEEKDAY_SIZE.val(data['day']['size']);
        CLOCK_FORMAT1.val(data['clock']['format']);
        CLOCK_SIZE1.val(data['clock']['size']);
        setBnt(CLOCK_FORMAT2_ENABLE, data['date']['enabled']);
        CLOCK_FORMAT2.val(data['date']['format']);
        CLOCK_SIZE2.val(data['date']['size']);
        CLOCK_OFFSET.val(data['alarm']['offset']);
        CLOCK_MIN.val(minToTime(data['alarm']['min']));
        setBnt(CLOCK_MIN_ENABLE, data['alarm']['min'] != -1);
        CLOCK_MAX.val(minToTime(data['alarm']['max']));
        setBnt(CLOCK_MAX_ENABLE, data['alarm']['max'] != -1);
        if (data['alarm']['days'] == 'Days.Weekdays') CLOCK_DAYS_1.prop('checked', true);
        else if (data['alarm']['days'] == 'Days.Weekends') CLOCK_DAYS_2.prop('checked', true);
        else if (data['alarm']['days'] == 'Days.Both') CLOCK_DAYS_3.prop('checked', true);
    });
}

GCAL_RESET_FORM.submit(function ()
{
    $.post('/api/resetgcal', function (data)
    {
        loadStatus();
        loadSettings();
    });
    return false;
});

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
    loadSettings();
});
TAB_GCAL.on('show.bs.tab', function ()
{
    console.log('Tab gcal');
    loadSettings();
});

if (document.location.toString().match('#'))
{
    $('.nav-tabs a[href="#' + document.location.toString().split('#')[1] + '"]').tab('show');
}
$('.nav-tabs a').on('shown.bs.tab', function (e)
{
    loadStatus();
    window.location.hash = e.target.hash;
});

