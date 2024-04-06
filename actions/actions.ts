'use server'
import prisma from '@/lib/prisma'

export async function getUsers() {
	return prisma.user.findMany();
}

export async function create() {
	return await prisma.user.create({
		data: {
			email: 'efef@gmail.com',
			name: 'ouwdwdi',
		},
	})
}