from typing import Annotated

from fastapi import Depends

from src.utils.unitofwork import InterfaceUnitOfWork, UnitOfWork

UOWDep = Annotated[InterfaceUnitOfWork, Depends(UnitOfWork)]
