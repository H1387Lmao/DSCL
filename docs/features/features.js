const features = [
    {
        title: "Command System",
        description: "Creating commands is simple with the `cmd` keyword. DSCL handles the `async def` and `ctx` boilerplate for you.",
        dscl: `cmd greet(User: member) -> bot {\n    await this->respond("Hi %s" % member)\n}`,
        python: `@bot.slash_command()\nasync def greet(ctx, member: discord.Member):\n    await ctx.respond(f"Hi {member}")`
    },
    {
        title: "Conditional Logic",
        description: "DSCL supports `if`, `elseif`, and `else` blocks for flow control, using a clean brace-based syntax.",
        dscl: `if i == 67 {\n    print("SIX SEVENNNN")\n} elseif i == 21 {\n    print("9+10")\n} else {\n    print(i)\n}`,
        python: `if i == 67:\n    print("SIX SEVENNNN")\nelif i == 21:\n    print("9+10")\nelse:\n    print(i)`
    },
    {
        title: "Variables & Math",
        description: "Use `mut` for variables and `const` for constants. Supports standard mathematical expressions and grouping.",
        dscl: `mut b = (3 + 2) * 2\nconst TOKEN = "XYZ"`,
        python: `b = (3 + 2) * 2\nTOKEN = "XYZ"`
    },
    {
        title: "Loops (For & While)",
        description: "Iterate through ranges with `->` or use `while` loops for conditional repetition.",
        dscl: `for i: 1->100 {\n    print(i)\n}\n\nwhile b != 0 {\n    b = b - 1\n}`,
        python: `for i in range(1, 100):\n    print(i)\n\nwhile b != 0:\n    b -= 1`
    },
    {
        title: "Asynchronous Functions",
        description: "Define non-blocking logic using `async fn`. Use the `await` keyword to handle promises.",
        dscl: `async fn test_async() {\n    print("hello!")\n}\n\nawait test_async()`,
        python: `async def test_async():\n    print("hello!")\n\nawait test_async()`
    },
    {
        title: "Lambda Functions",
        description: "Assign logic to variables using the `fn` keyword, perfect for callbacks and button events.",
        dscl: `mut a = fn() {\n    print("Clicked!")\n}\n\na()`,
        python: `def lambda_1():\n    print("Clicked!")\na = lambda_1\n\na()`
    },
    {
        title: "User Databases",
        description: "Manage persistent data easily using `new UserDatabase()`. DSCL maps these to simple dictionary-like access.",
        dscl: `caught = new UserDatabase()\nconst user = tostr(this->user->id)\nconst inv = caught[user]`,
        python: `caught = UserDatabase()\nuser = str(ctx.author.id)\ninv = caught[user]`
    },
    {
        title: "UI Components",
        description: "Build Discord UI layouts using `View` and `Container`. DSCL supports native `Row` and `Text` placement.",
        dscl: `this->respond(\n    view=View(\n        Container(\n            Text("Inventory:"),\n            color=Colors->Red\n        )\n    )\n)`,
        python: `await ctx.respond(\n    view=View(\n        Container(\n            Text("Inventory:"), \n            color=Colors.Red\n        )\n    )\n)`
    },
    {
        title: "Packages & Imports",
        description: "Access external modules like `random` or `time` using the `use` keyword.",
        dscl: `use pkg::discord\nuse random\n\nprint(random->randint(1, 500))`,
        python: `from dscl.discord import *\nimport random\n\nprint(random.randint(1, 500))`
    }
];
