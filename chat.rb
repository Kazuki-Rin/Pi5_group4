require 'rubygems'
require 'mqtt'

print "GROUP 4"
name = gets.chomp

broker_ip = '127.0.0.1'
topic = 'chat/room1'

begin
	client = MQTT::Client.connect(broker_ip)
	puts "Da ket noi thanh cong! Go tin nhan va nhan Enter (Go 'exit' de thoat)"

	Thread.new do
		client.get(topic) do |t, message|
			print "\r[Tin nhan moi] #{message}\n"
		end
	end

	loop do
		msg = gets.chomp
		break if msg.downcase == 'exit'
		client.publish(topic, "#{name}: #{msg}")
	end

	client.disconnect
	puts "Da ngat ket noi"

rescue StandardError => e
	puts "Loi ket noi: #{e.message}"
end

