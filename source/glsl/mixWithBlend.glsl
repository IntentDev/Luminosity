uniform vec2 modeOpacity[16];
uniform float uOutputLevel;


layout(location = 0) out vec4 fragColor;

vec4 Mode(in vec4 base, in vec4 blend, in float opacity, in float mode)
{
	vec4 white = vec4(1.0,1.0,1.0,1.0);
	vec4 lumCoeff = vec4(0.2125,0.7154,0.0721,1.0);

	if (mode <= 0)
	{
		//normal

		vec4 baseA = base * (1-blend.a);
		vec4 result = baseA + blend;
		return mix(base, result, opacity);
	}

		else if (mode == 1)
	{
		//average
		vec4 result = (base + blend) * 0.5;
		return mix(base, result, opacity);
	}

		else if (mode == 2)
	{
		// behind
		vec4 result = (base.a == 0.0) ? blend : base;
		return mix(base, result, opacity);
	}

		else if (mode == 3)
	{
		//cross
		vec4 result;
		result = blend;
		return mix(base, result, opacity);
	}

		else if (mode == 4)
	{
		//darken
		vec4 result = min(blend, base);
		return mix(base, result, opacity);
	}

		else if (mode == 5)
	{
		//lighten
		vec4 result = max(blend, base);
		return mix(base, result, opacity);
	}

		else if (mode == 6)
	{
		//multiply
		vec4 result = blend * base;
		return mix(base, result, opacity);
	}

		else if (mode == 7)
	{
		//screen
		vec4 result = white - ((white - blend) * (white - base));
		return mix(base, result, opacity);
	}

		else if (mode == 8)
	{
		//color burn
		vec4 result = white - (white - base) / blend;
		return mix(base, result, opacity);
	}

		else if (mode == 9)
	{
		//color dodge
		vec4 result = base / (white - blend);
		//return mix(base, result, opacity);
		return mix(base, vec4(result.rgb, blend.a), opacity);
	}

		else if (mode == 10)
	{
		//overlay
		vec4 result;
		float luminance = dot(base, lumCoeff);
		if (luminance < 0.45)
			result = 2.0 * blend * base;
			else if (luminance > 0.55)
			result = white - 2.0 * (white - blend) * (white - base);
		else
		{
			vec4 result1 = 2.0 * blend * base;
			vec4 result2 = white - 2.0 * (white - blend) * (white - base);
			result = mix(result1, result2, (luminance - 0.45) * 10.0);
		}
		return mix(base, result, opacity);
	}

		else if (mode == 11)
	{
		//soft light
		vec4 result = 2.0 * base * blend + base * base - 2.0 * base * base * blend;
		return mix(base, result, opacity);
	}

		else if (mode == 12)
	{
		//hard light
		vec4 result;
		float luminance = dot(blend, lumCoeff);
		if (luminance < 0.45)
			result = 2.0 * blend * base;
		else if (luminance > 0.55)
			result = white - 2.0 * (white - blend) * (white - base);
		else
			{
				vec4 result1 = 2.0 * blend * base;
				vec4 result2 = white - 2.0 * (white - blend) * (white - base);
				result = mix(result1, result2, (luminance - 0.45) * 10.0);
			}
		return mix(base, result, opacity);
	}

		else if (mode == 13)
	{
		//add
		vec4 result = blend + base;
		return mix(base, result, opacity);
	}

		else if (mode == 14)
	{
		//subtract
		vec4 result = blend - base;
		return mix(base, vec4(result.rgb, blend.a), opacity);
	}

		else if (mode == 15)
	{
		//difference
		vec4 result = abs(blend - base);
		return mix(base, vec4(result.rgb, blend.a), opacity);
	}

		else if (mode == 16)
	{
		//inverse difference
		vec4 result = white - abs(white - base - blend);
		return mix(base, vec4(result.rgb, blend.a), opacity);
	}

		else if (mode >= 17)
	{
		//exclusion
		vec4 result = base + blend - (2.0 * base * blend);
		return mix(base, vec4(result.rgb, blend.a), opacity);
	}

}

void main()
{
	vec2 texCoord = vec2(0.0);
	vec4 mix = vec4(0.0);

	for(int i=0; i < TD_NUM_2D_INPUTS; i++)
	{
		vec4 blend = texture(sTD2DInputs[i], vUV.st);
		mix = Mode(mix,blend,modeOpacity[i].y,int(modeOpacity[i].x));
	}

	fragColor = mix;
}
