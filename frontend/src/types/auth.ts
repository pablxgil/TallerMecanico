export type Role = 'administrador' | 'recepcionista' | 'asesor_servicio' | 'tecnico' | 'usuario' | 'sistema'
export interface User { id: number; full_name: string; email: string; role: Role; is_active: boolean }
export interface LoginResponse { access_token: string; token_type: string; user: User }

