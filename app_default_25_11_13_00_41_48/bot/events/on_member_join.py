async def on_member_join_handler(bot, member):
    # Assign default role
    default_role_name = "Member"
    role = None
    for r in member.guild.roles:
        if r.name == default_role_name:
            role = r
            break
    if role:
        await member.add_roles(role)
    await member.send(f"Welcome to {member.guild.name}, {member.name}!")
    # Optionally notify admins
