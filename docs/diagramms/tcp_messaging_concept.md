@startuml
hnote across: worker got request to generate a new messagepart
participant worker as w
participant chatgpt4all as c
w -> c : client establish connection
activate c
c -> w : port open for command
deactivate c
activate w
w -> c : generate messagepart of message(id)
note across: api will keep generator saved under id for a set amount of time or until generation finished
deactivate w
activate c
loop timeout or wordcount not reached
c -> w : send word
deactivate c
end
w -> c : stop generating client connection closed
@enduml
