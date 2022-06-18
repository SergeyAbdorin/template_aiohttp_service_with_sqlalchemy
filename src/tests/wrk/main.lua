require "app_requests"

local counter = 1
local requests_count = #app_requests

local getNextPayload = function()
    payload = app_requests[(counter % requests_count) + 1]

    method = payload[1]
    path = payload[2]
    headers = payload[3]
    body = payload[4]

    return method, path, headers, body
end

request = function()
    counter = counter + 1

    method, path, headers, body = getNextPayload()

    return wrk.format(method, path, headers, body)
end

done = function(summary, latency, requests)
    io.write("------------------------------\n")
    io.write(string.format("Total requests: %d\n", summary.requests))
    errors_count = 
        summary.errors.connect +
        summary.errors.read +
        summary.errors.write +
        summary.errors.status +
        summary.errors.timeout
    io.write(string.format("Total errors: %d\n", errors_count))
    io.write("Errors info: \n")
    io.write(string.format("\t connect errors: %d\n", summary.errors.connect))
    io.write(string.format("\t read errors:    %d\n", summary.errors.read))
    io.write(string.format("\t write errors:   %d\n", summary.errors.write))
    io.write(string.format("\t status errors:  %d\n", summary.errors.status))
    io.write(string.format("\t timeout errors: %d\n", summary.errors.timeout))
    io.write("------------------------------\n")
    for _, p in pairs({ 50, 70, 90, 95, 99, 99.9, 99.99, 99.999 }) do
       n = latency:percentile(p)
       io.write(string.format("%g%%:  %d ms\n", p, n / 1000))
    end
end
