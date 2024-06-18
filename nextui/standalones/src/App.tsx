import UsersMultiselect from "./components/selects/UsersMutliselect"
import users from '../src/data/users.json'

function App() {
  return (
    <div className="flex flex-col h-svh p-2">
      <div>
        <p className="font-bold bg-gray-300 p-3 border border-gray-300">Multiselect</p>
        <div className="p-4">
          <UsersMultiselect data={users} />
        </div>
      </div>
    </div>
  )
}

export default App
