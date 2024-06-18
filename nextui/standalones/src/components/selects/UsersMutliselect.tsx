import { User } from '../../types/users'
import { Select, SelectItem } from '@nextui-org/react'

// to allow multiple selection, we just have to set selectionMode="multiple" in select

type UsersMutliselectProps = {
    data: User[]
}

const UsersMultiselect = ({data}: UsersMutliselectProps) => {
    console.log(data)

    return <>
    <Select
        items={data}
        label="User"
        placeholder='Select User'
        className='max-w-xs'
        selectionMode='multiple'
        >
            {(user) => <SelectItem key={user.id}>{user.name}</SelectItem>}
    </Select>
    </>
}

export default UsersMultiselect