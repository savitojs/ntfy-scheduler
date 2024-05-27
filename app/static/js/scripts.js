$(document).ready(function() {
    fetchDefaults();
    fetchTopics();
    fetchServers();
    fetchScheduledMessages();

    const now = new Date();
    const localDatetime = new Date(now.getTime() - (now.getTimezoneOffset() * 60000)).toISOString().slice(0, 16);
    $("#datetime").val(localDatetime);

    // Add event listener for the "Send Now" checkbox
    $("#send-now").change(function() {
        toggleDatetimeInput();
    });

    // Message resizeable
    $(".resizable").resizable({
        handles: "se", // Only allow resizing from the bottom-right corner
        minWidth: 200,
        minHeight: 100
    });

    // Tootip

    $('[data-toggle="tooltip"]').tooltip(); 

    // Function to toggle the datetime input field
    function toggleDatetimeInput() {
        if ($("#send-now").is(":checked")) {
            $("#datetime").prop("disabled", true);
        } else {
            $("#datetime").prop("disabled", false);
        }
    }

    // Initialize the state of the datetime input field on page load
    toggleDatetimeInput();

    $("#schedule-link").click(function() {
        $("#schedule-message-section").removeClass("custom-hidden");
        $("#scheduled-messages-section").addClass("custom-hidden");
        $("#sent-messages-section").addClass("custom-hidden");
        $("#manage-topics-section").addClass("custom-hidden");
        $("#manage-servers-section").addClass("custom-hidden");
    });

    $("#view-scheduled-link").click(function() {
        $("#schedule-message-section").addClass("custom-hidden");
        $("#scheduled-messages-section").removeClass("custom-hidden");
        $("#sent-messages-section").addClass("custom-hidden");
        $("#manage-topics-section").addClass("custom-hidden");
        $("#manage-servers-section").addClass("custom-hidden");
        fetchScheduledMessages();
    
        // Fetch events and initialize calendar
        fetchScheduledEvents().then(function(events) {
            initializeCalendar(events, 'scheduled-calendar');
        });
    });

    $("#view-sent-link").click(function() {
        $("#schedule-message-section").addClass("custom-hidden");
        $("#scheduled-messages-section").addClass("custom-hidden");
        $("#sent-messages-section").removeClass("custom-hidden");
        $("#manage-topics-section").addClass("custom-hidden");
        $("#manage-servers-section").addClass("custom-hidden");
        fetchSentMessages();
    
        // Ensure the calendar container is visible before initializing
        setTimeout(function() {
            fetchSentEvents().then(function(events) {
                initializeCalendar(events, 'sent-calendar');
            });
        }, 100); // Adjust the timeout duration if necessary
    });

    $("#manage-topics-link").click(function() {
        $("#schedule-message-section").addClass("custom-hidden");
        $("#scheduled-messages-section").addClass("custom-hidden");
        $("#sent-messages-section").addClass("custom-hidden");
        $("#manage-topics-section").removeClass("custom-hidden");
        $("#manage-servers-section").addClass("custom-hidden");
        fetchTopics();
    });

    $("#manage-servers-link").click(function() {
        $("#schedule-message-section").addClass("custom-hidden");
        $("#scheduled-messages-section").addClass("custom-hidden");
        $("#sent-messages-section").addClass("custom-hidden");
        $("#manage-topics-section").addClass("custom-hidden");
        $("#manage-servers-section").removeClass("custom-hidden");
        fetchServers();
    });

    $("#interval").change(function() {
        if ($(this).val() === "custom") {
            $(".custom-interval").removeClass("custom-hidden");
        } else {
            $(".custom-interval").addClass("custom-hidden");
        }
    });

    // Initialize flatpickr for datetime input
    $("#datetime").flatpickr({
        enableTime: true,
        dateFormat: "Y-m-d\\TH:i"
    });

    $("#schedule-form").submit(function(event) {
        event.preventDefault();
        const interval = $("#interval").val();
        const customDays = interval === "custom" ? $("#custom-days").val() : "";
        const sendNow = $("#send-now").is(":checked");
        const timezone = Intl.DateTimeFormat().resolvedOptions().timeZone;

        let data = {
            message: $("#message").val(),
            server: $("#server").val(),
            topic: $("#topic").val(),
            interval: interval,
            custom_days: customDays,
            timezone: timezone,
            header_title: $("#header-title").val(),
            header_priority: $("#header-priority").val(),
            header_tags: $("#header-tags").val()
        };

        if (sendNow) {
            const localNow = new Date();
            data.datetime = localNow.toISOString();
        } else {
            const localDatetimeString = $("#datetime").val();
            const localDatetime = new Date(localDatetimeString);
            data.datetime = localDatetime.toISOString();
        }

        $.ajax({
            url: '/schedule',
            method: 'POST',
            data: data,
            success: function(response) {
                showNotification(response);
                fetchScheduledMessages();
                clearForm("#schedule-form");
            }
        });
    });

    $("#add-topic-form").submit(function(event) {
        event.preventDefault();
        $.ajax({
            url: '/add_topic',
            method: 'POST',
            data: {
                name: $("#new-topic").val()
            },
            success: function(response) {
                showNotification(response);
                fetchTopics();
                clearForm("#add-topic-form");
            }
        });
    });

    $("#add-server-form").submit(function(event) {
        event.preventDefault();
        $.ajax({
            url: '/add_server',
            method: 'POST',
            data: {
                address: $("#new-server").val()
            },
            success: function(response) {
                showNotification(response);
                fetchServers();
                clearForm("#add-server-form");
            }
        });
    });

    $(document).on('change', '.default-topic-checkbox', function() {
        const topic = $(this).data('topic');
        if (this.checked) {
            setDefaultTopic(topic);
        }
    });

    $(document).on('change', '.default-server-checkbox', function() {
        const server = $(this).data('server');
        if (this.checked) {
            setDefaultServer(server);
        }
    });

    $(document).on('click', '.delete-btn', function() {
        const id = $(this).data('id');
        $.ajax({
            url: `/delete/${id}`,
            method: 'DELETE',
            success: function(response) {
                showNotification(response);
                fetchScheduledMessages();
            }
        });
    });

    $(document).on('click', '.delete-topic-btn', function() {
        const id = $(this).data('id');
        $.ajax({
            url: `/delete_topic/${id}`,
            method: 'DELETE',
            success: function(response) {
                showNotification(response);
                fetchTopics();
            }
        });
    });

    $(document).on('click', '.delete-server-btn', function() {
        const id = $(this).data('id');
        $.ajax({
            url: `/delete_server/${id}`,
            method: 'DELETE',
            success: function(response) {
                showNotification(response);
                fetchServers();
            }
        });
    });

    $(document).on('click', '.edit-btn', function() {
        const id = $(this).data('id');
        const row = $(this).closest('tr');
        const message = row.find('.message-input').val();
        const datetime = row.find('.datetime-input').val();
        const server = row.find('.server-select').val();
        const topic = row.find('.topic-select').val();
        const interval = row.find('.interval-select').val();
        const customDays = interval === "custom" ? row.find('.custom-days-input').val() : "";
        const timezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
        const headers = {
            title: row.find('.header-title-input').val(),
            priority: row.find('.header-priority-input').val(),
            tags: row.find('.header-tags-input').val()
        };

        $.ajax({
            url: `/edit/${id}`,
            method: 'PUT',
            data: {
                message: message,
                datetime: datetime,
                server: server,
                topic: topic,
                interval: interval,
                custom_days: customDays,
                timezone: timezone,
                headers: JSON.stringify(headers)
            },
            success: function(response) {
                showNotification(response);
                fetchScheduledMessages();
            }
        });
    });

    function fetchDefaults() {
        $.get('/default_topic', function(data) {
            $('#topic').val(data.default_topic);
            $('#default-topic').val(data.default_topic);
            $('.default-topic-checkbox').prop('checked', false);
            $(`.default-topic-checkbox[data-topic="${data.default_topic}"]`).prop('checked', true);
        });
        $.get('/default_server', function(data) {
            $('#server').val(data.default_server);
            $('#default-server').val(data.default_server);
            $('.default-server-checkbox').prop('checked', false);
            $(`.default-server-checkbox[data-server="${data.default_server}"]`).prop('checked', true);
        });
    }

    function fetchTopics() {
        $.get('/topics', function(data) {
            $('#topic').empty();
            $('#topics-table tbody').empty();
            data.topics.forEach(function(topic) {
                $('#topic').append(`<option value="${topic.name}">${topic.name}</option>`);
                $('#topics-table tbody').append(`
                    <tr>
                        <td>${topic.id}</td>
                        <td>${topic.name}</td>
                        <td><input type="checkbox" class="default-topic-checkbox" data-topic="${topic.name}"></td>
                        <td><button class="btn btn-danger delete-topic-btn" data-id="${topic.id}">Delete</button></td>
                    </tr>
                `);
            });
            fetchDefaults();
        });
    }

    function fetchServers() {
        $.get('/servers', function(data) {
            $('#server').empty();
            $('#servers-table tbody').empty();
            data.servers.forEach(function(server) {
                $('#server').append(`<option value="${server.address}">${server.address}</option>`);
                $('#servers-table tbody').append(`
                    <tr>
                        <td>${server.id}</td>
                        <td>${server.address}</td>
                        <td><input type="checkbox" class="default-server-checkbox" data-server="${server.address}"></td>
                        <td><button class="btn btn-danger delete-server-btn" data-id="${server.id}">Delete</button></td>
                    </tr>
                `);
            });
            fetchDefaults();
        });
    }

    function fetchScheduledMessages() {
        $.get('/scheduled', function(data) {
            $('#scheduled-messages tbody').empty();
            data.messages.forEach(function(message) {
                const localDatetime = convertUTCToLocal(message.datetime);
                const localNextSchedule = message.next_schedule ? formatLocalDateTimeForDisplay(message.next_schedule) : '';
    
                const headers = JSON.parse(message.headers);
                $('#scheduled-messages tbody').append(`
                    <tr data-id="${message.id}">
                        <td>${message.id}</td>
                        <td><input type="text" class="form-control message-input" value="${message.message}"></td>
                        <td><input type="datetime-local" class="form-control datetime-input" value="${localDatetime}"></td>
                        <td>${message.interval ? localNextSchedule : ''}</td>
                        <td>
                            <select class="form-control server-select">
                                <!-- Server options will be populated dynamically -->
                            </select>
                        </td>
                        <td>
                            <select class="form-control topic-select">
                                <!-- Topic options will be populated dynamically -->
                            </select>
                        </td>
                        <td>
                            <select class="form-control interval-select">
                                <option value="">None</option>
                                <option value="daily" ${message.interval === 'daily' ? 'selected' : ''}>Daily</option>
                                <option value="weekly" ${message.interval === 'weekly' ? 'selected' : ''}>Weekly</option>
                                <option value="monthly" ${message.interval === 'monthly' ? 'selected' : ''}>Monthly</option>
                                <option value="custom" ${message.interval === 'custom' ? 'selected' : ''}>Custom</option>
                            </select>
                            <input type="number" class="form-control custom-days-input ${message.interval !== 'custom' ? 'd-none' : ''}" value="${message.custom_days}">
                        </td>
                        <td>
                            <input type="text" class="form-control header-title-input" value="${headers.Title || ''}">
                            <input type="text" class="form-control header-priority-input" value="${headers.Priority || ''}">
                            <input type="text" class="form-control header-tags-input" value="${headers.Tags || ''}">
                        </td>
                        <td>
                            <button class="btn btn-secondary edit-btn" data-id="${message.id}">Save</button>
                            <button class="btn btn-danger delete-btn" data-id="${message.id}">Delete</button>
                        </td>
                    </tr>
                `);
                populateServerOptions(message.id, message.server);
                populateTopicOptions(message.id, message.topic);
            });
        });
    }    
    
    function convertUTCToLocal(utcDatetimeStr) {
        const utcDatetime = new Date(utcDatetimeStr);
        const localDatetime = new Date(utcDatetime.getTime() - (utcDatetime.getTimezoneOffset() * 60000));
        return localDatetime.toISOString().slice(0, 16); // This format is suitable for input[type="datetime-local"]
    }
    
    function formatLocalDateTimeForDisplay(localDatetimeStr) {
        const localDatetime = new Date(localDatetimeStr);
        const options = { year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit', hour12: true };
        return localDatetime.toLocaleString('en-US', options);
    }
    
        
    function fetchScheduledEvents() {
        return $.get('/scheduled').then(function(data) {
            return data.messages.map(function(message) {
                return {
                    id: message.id,
                    title: message.message,
                    start: message.datetime,
                    extendedProps: {
                        server: message.server,
                        topic: message.topic,
                        interval: message.interval
                    }
                };
            });
        });
    }

    function fetchSentEvents() {
        return $.get('/sent').then(function(data) {
            return data.messages.map(function(message) {
                return {
                    id: message.id,
                    title: message.message,
                    start: message.datetime,
                    extendedProps: {
                        server: message.server,
                        topic: message.topic,
                        interval: message.interval
                    }
                };
            });
        });
    }
    function initializeCalendar(events, calendarId) {
        var calendarEl = document.getElementById(calendarId);
        if (calendarEl) {
            var calendar = new FullCalendar.Calendar(calendarEl, {
                initialView: 'dayGridMonth',
                events: events,
                eventClick: function(info) {
                    // Handle event click, e.g., display event details or open edit form
                    alert('Message: ' + info.event.title);
                }
            });
            calendar.render();
        } else {
            console.error("Calendar element not found");
        }
    }

    function fetchSentMessages() {
        $.get('/sent', function(data) {
            $('#sent-messages tbody').empty();
            data.messages.forEach(function(message) {
                const localDatetime = new Date(message.datetime).toLocaleString();  // Correcting the time display
                const localSentAt = new Date(message.sent_at).toLocaleString();  // Correcting the time display
                const headers = JSON.parse(message.headers);  // Parse the headers
                $('#sent-messages tbody').append(`
                    <tr data-id="${message.id}">
                        <td>${message.id}</td>
                        <td>${message.message}</td>
                        <td>${localDatetime}</td>
                        <td>${message.server}</td>
                        <td>${message.topic}</td>
                        <td>${localSentAt}</td>
                        <td>
                            <input type="text" class="form-control header-title-input" value="${headers.Title || ''}" readonly>
                            <input type="text" class="form-control header-priority-input" value="${headers.Priority || ''}" readonly>
                            <input type="text" class="form-control header-tags-input" value="${headers.Tags || ''}" readonly>
                        </td>
                    </tr>
                `);
            });
        });
    }    

    function setDefaultTopic(topic) {
        $.ajax({
            url: '/set_default_topic',
            method: 'POST',
            data: {
                topic: topic
            },
            success: function(response) {
                showNotification(response);
                fetchDefaults();
            }
        });
    }

    function setDefaultServer(server) {
        $.ajax({
            url: '/set_default_server',
            method: 'POST',
            data: {
                server: server
            },
            success: function(response) {
                showNotification(response);
                fetchDefaults();
            }
        });
    }

    function populateServerOptions(messageId, selectedServer) {
        $.get('/servers', function(data) {
            const select = $(`#scheduled-messages tbody tr[data-id="${messageId}"] .server-select`);
            select.empty();
            data.servers.forEach(function(server) {
                select.append(`<option value="${server.address}" ${server.address === selectedServer ? 'selected' : ''}>${server.address}</option>`);
            });
        });
    }

    function populateTopicOptions(messageId, selectedTopic) {
        $.get('/topics', function(data) {
            const select = $(`#scheduled-messages tbody tr[data-id="${messageId}"] .topic-select`);
            select.empty();
            data.topics.forEach(function(topic) {
                select.append(`<option value="${topic.name}" ${topic.name === selectedTopic ? 'selected' : ''}>${topic.name}</option>`);
            });
        });
    }

    function showNotification(message) {
        $("#notification").text(message).removeClass("custom-hidden");
        setTimeout(function() {
            $("#notification").addClass("custom-hidden");
        }, 3000);
    }

    function clearForm(formSelector) {
        $(formSelector).find("input[type=text], input[type=datetime-local], input[type=number], select").val("");
        $(formSelector).find("input[type=checkbox]").prop("checked", false);
        $(formSelector).find(".custom-interval").addClass("custom-hidden");
    }
});