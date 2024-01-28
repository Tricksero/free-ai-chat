@startuml
participant Database
participant Backend
participant Frontend

Backend <- Frontend: submits edited question with new question text
Activate Backend
Activate Frontend
Database <- Backend: Update Question
Backend -> Frontend: First part of response with state(finished/unfinished/error)
Deactivate Backend
loop generate
alt state(unfinished)
Backend <- Frontend: Keep generation alive
Activate Backend
Backend -> Database: Update question response data
Backend -> Frontend: Added parts to response with state(finished/unfinished/error)
Deactivate Backend
Deactivate Frontend
end
end
@enduml
